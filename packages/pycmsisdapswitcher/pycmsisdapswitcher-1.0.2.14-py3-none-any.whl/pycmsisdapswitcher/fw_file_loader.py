
'''
Helper module: loads the new firmware file into the target
'''

import sys
import time
import os
import zlib
import array
from typing import Tuple
import struct
import threading

import usb.core
import usb.util
from intelhex import IntelHex

from pycmsisdapswitcher import dictionaries
from .print_utils import print_verbose
# from .dictionaries import app_image_info
from .exit_codes import SWITCH_APP_ERROR


# Command constants
commands = {
    'ENTER_BOOT_MODE': 0xEB,
    'JUMP_TO_APP': 0xEC,
    'ERASE_FLASH': 0xE2,
    'ERASE_APPLICATION': 0xFA,
    'WRITE_PAGE': 0xE3,
    'READ_CRC32': 0xE5,
    'SOFTWARE_RESET': 0xED,
}

# USB endpoint numbers
endpoints_numbers = {
    # NOTE: directions referred to the host
    'COMMAND_OUT_MPLAB_FW_TYPE': 0x02,
    'COMMAND_OUT_CMSIS_DAP_V2_FW_TYPE': 0x01,
    'COMMAND_OUT_MPLAB_BOOT': 0x02,
    'COMMAND_IN_MPLAB_BOOT': 0x81,
}

# USB transmit offsets
usb_transmit_offsets = {
    'COMMAND_OPCODE': 0,
    'FIRST_ARGUMENT': 1,
    'SECOND_ARGUMENT': 13,
}

# USB receive offsets
usb_receive_offsets = {
    'COMMAND_OPCODE_ECHO': 0,
    'ERASE_FLASH_ERROR_CODE': 2,
    'WRITE_PAGE_ERROR_CODE': 13,
}

# Timeout values in milliseconds
timeouts_ms = {
    'USB_COMM': 4_000,
    'USB_ENUM': 30_000,
    'USB_DE_ENUM': 30_000,
    'ERASE_FLASH': 60_000,
    'WRITE_FLASH_PAGE': 1_000,
    'READ_CRC32': 5_000,
}

# Other constants
BOOTLOADER_IMAGE_SIZE_IN_BYTES = 48 * 1024
APPLICATION_IMAGE_SIZE_IN_BYTES = (
    2 * 1024 * 1024) - BOOTLOADER_IMAGE_SIZE_IN_BYTES
BOOTLOADER_IMAGE_CRC_BASE_ADDRESS = BOOTLOADER_IMAGE_SIZE_IN_BYTES - 4
APPLICATION_IMAGE_CRC_BASE_ADDRESS = APPLICATION_IMAGE_SIZE_IN_BYTES - 4
ERASE_STATUS_SIZE_IN_BYTES = 3
WRITE_PAGE_STATUS_SIZE_IN_BYTES = 14
NO_COMMAND_ERROR = 0
FLASH_PAGE_SIZE_IN_BYTES = 512
APPLICATION_START_ADDRESS = 0x0040_C000
WRITE_FLASH_PAGE_COMMAND_SIZE_IN_BYTES = 525
FLASH_ADDRESS_SIZE_IN_BYTES = 4
READ_CRC32_STATUS_SIZE_IN_BYTES = 256
CRC32_SIZE_IN_BYTES = 4


class FWFileLoader:
    '''
    Provides methods to load the new firmware file into the target
    '''

    def __init__(self,
                 target: str,
                 usb_device: usb.core.Device,
                 current_fw_type: str,
                 new_fw_file_path: str,
                 new_fw_type: str) -> None:
        self.target = target
        self.usb_device = usb_device
        self.current_fw_type = current_fw_type
        self.new_fw_file_path = new_fw_file_path
        self.new_fw_type = new_fw_type

    def _get_pid_dictionary_keys(self, what: str) -> Tuple[str, str]:
        '''
        Sets PID dictionary keys and sub-keys
        # NOTE: the application PIDs are tuples, while the bootloader has an unique PID
        '''
        if self.target == 'evalboard':
            target_key = "EVAL_BOARD"
        else:
            target_key = "PICKIT_BASIC"

        if what == 'mplab_app':
            target_subkey = "MPLAB_APP_PID"
        elif what == 'cmsis_v2_app':
            target_subkey = "CMSIS_V2_APP_PID"
        else:
            target_subkey = "MPLAB_BOOT_PID"

        return target_key, target_subkey

    def _did_it_de_enumerate(self, what: str):
        '''
        Keeps finding the target in application or boot mode until it disappears or time-out happens
        :return: True if application or boot de-enumerated in time, else (timeout) False
        '''

        # Get PID dictionary keys and sub-keys
        # NOTE: the application PIDs are tuples, while the bootloader has an unique PID
        target_key, target_subkey = self._get_pid_dictionary_keys(what)

        start_time_s = time.perf_counter()  # In fractional seconds

        it_de_enumerated = False
        while not it_de_enumerated:
            if isinstance(dictionaries.app_pids[target_key][target_subkey], tuple):
                device_list = []
                for pid in dictionaries.app_pids[target_key][target_subkey]:
                    self.usb_device = usb.core.find(
                        idVendor=dictionaries.vids['MCHP'],
                        idProduct=pid,
                        find_all=False)

                    if self.usb_device:
                        device_list.append(self.usb_device)

                if len(device_list) == 0:
                    it_de_enumerated = True
                    break
            else:
                self.usb_device = usb.core.find(
                    idVendor=dictionaries.vids['MCHP'],
                    idProduct=dictionaries.app_pids[target_key][target_subkey],
                    find_all=False)

                if not self.usb_device:
                    it_de_enumerated = True
                    break

            elapsed_time_s = time.perf_counter() - start_time_s
            if elapsed_time_s >= timeouts_ms['USB_DE_ENUM'] / 1_000:
                break

        return it_de_enumerated

    def _did_it_enumerate(self, what: str):
        '''
        Keeps looking for the target in application or boot mode until it finds it or times-out
        :return: True if the application or boot enumerated in time, else (timeout) False
        '''
        # Get PID dictionary keys and sub-keys
        # NOTE: the application PIDs are tuples, while the bootloader has an unique PID
        target_key, target_subkey = self._get_pid_dictionary_keys(what)

        start_time_s = time.perf_counter()  # In fractional seconds

        it_enumerated = False
        while not it_enumerated:
            elapsed_time_s = time.perf_counter() - start_time_s
            if elapsed_time_s >= timeouts_ms['USB_DE_ENUM'] / 1_000:
                break

            if isinstance(dictionaries.app_pids[target_key][target_subkey], tuple):
                for pid in dictionaries.app_pids[target_key][target_subkey]:
                    self.usb_device = usb.core.find(
                        idVendor=dictionaries.vids['MCHP'],
                        idProduct=pid,
                        find_all=False)

                    if self.usb_device:
                        # Check that the active configuration is ready
                        try:
                            self.usb_device.get_active_configuration()
                        except:
                            continue
                        it_enumerated = True
                        break

            else:
                self.usb_device = usb.core.find(
                    idVendor=dictionaries.vids['MCHP'],
                    idProduct=dictionaries.app_pids[target_key][target_subkey],
                    find_all=False)

                if self.usb_device:
                    # Check that the active configuration is ready
                    try:
                        configuration = self.usb_device.get_active_configuration()
                        if not configuration:
                            continue
                    except:
                        continue
                    it_enumerated = True
                    break

        return it_enumerated

    def _enter_boot_mode_mplab(self) -> None:
        '''
        Sends to mplab type application the command to enter boot mode \n
        Prints message and sys.exit(-1) if it fails
        '''
        command = bytearray(1)  # USB comm expects a sequence of bytes
        command[usb_transmit_offsets['COMMAND_OPCODE']
                ] = commands['ENTER_BOOT_MODE']

        try:
            bytes_to_endpoint = self.usb_device.write(endpoints_numbers['COMMAND_OUT_MPLAB_FW_TYPE'],
                                                      command,
                                                      timeouts_ms['USB_COMM'])
        except usb.core.USBError as usb_comm_error:
            print(f"\n Error: {print_verbose(self.target)} entering boot mode: "
                  f"{str(usb_comm_error)}.")
            sys.exit(SWITCH_APP_ERROR)

        if len(command) != bytes_to_endpoint:
            print(f"\n Error: {print_verbose(self.target)} entering boot mode: "
                  "write to endpoint size mismatch.")
            sys.exit(SWITCH_APP_ERROR)

        if not self._did_it_de_enumerate('mplab_app'):
            print(f"\n Error: {print_verbose(self.target)} entering boot mode: "
                  "the application didn't de-enumerate.")
            sys.exit(SWITCH_APP_ERROR)

        if not self._did_it_enumerate('boot'):
            print(F"\n Error: {print_verbose(self.target)} entering boot mode: "
                  "the bootloader didn't enumerate.")
            sys.exit(SWITCH_APP_ERROR)

        print("\n Bootloader mode entered.")

    def _enter_boot_mode_cmsisv2(self) -> None:
        '''
        Sends to cmsisv2 type application the command to enter boot mode,
        sys.exit(-1) if fails
        '''

        command_tuple = (0x80, 0x11, 0x00, 0x0B, 0x0E, 0x00,
                         0x01, 0x00, 0x01, 0x50, 0x00, 0x31, 0x72, 0x7C, 0x10)
        command = bytearray(command_tuple)

        try:
            bytes_to_endpoint = self.usb_device.write(endpoints_numbers['COMMAND_OUT_CMSIS_DAP_V2_FW_TYPE'],
                                                      command,
                                                      timeouts_ms['USB_COMM'])
        except usb.core.USBError as usb_comm_error:
            print(f"\n Error: {print_verbose(self.target)} entering boot mode: "
                  f"{str(usb_comm_error)}.")
            sys.exit(SWITCH_APP_ERROR)

        if len(command) != bytes_to_endpoint:
            print(f"\n Error: {print_verbose(self.target)} entering boot mode: "
                  "write to endpoint size mismatch.")
            sys.exit(SWITCH_APP_ERROR)

        if not self._did_it_de_enumerate('cmsis_v2_app'):
            print(f"\n Error: {print_verbose(self.target)} entering boot mode: "
                  "the application didn't de-enumerate.")
            sys.exit(SWITCH_APP_ERROR)

        if not self._did_it_enumerate('boot'):
            print(F"\n Error: {print_verbose(self.target)} entering boot mode: "
                  "the bootloader didn't enumerate.")
            sys.exit(SWITCH_APP_ERROR)

        print("\n Bootloader mode entered.")

    def _enter_boot_mode(self) -> None:
        '''
        Sends to the target the command to enter boot mode, de-enumerating from app mode,
        prints message and sys.exit(-1) if fails

        # NOTE: boot mode is persistent (power cycling won't exit it)
        '''

        if self.current_fw_type == 'mplab':
            self._enter_boot_mode_mplab()
        else:
            self._enter_boot_mode_cmsisv2()

    def _jump_to_app_mplab_boot(self):
        '''
        Sends to the target in MPLAB type bootloader mode \n
        the command to enter app_type mode, de-enumerating from boot mode \n

        Prints message and sys.exit(-1) if fails

         # NOTE: app mode is persistent (power cycling won't exit it)
        '''
        if (self.new_fw_type == 'mplab'):
            fw_type = "mplab_app"
        else:
            fw_type = "cmsis_v2_app"

        command = bytearray(1)  # USB comm expects a sequence of bytes
        command[usb_transmit_offsets['COMMAND_OPCODE']
                ] = commands['JUMP_TO_APP']

        try:
            bytes_to_endpoint = self.usb_device.write(endpoints_numbers['COMMAND_OUT_MPLAB_FW_TYPE'],
                                                      command,
                                                      timeouts_ms['USB_COMM'])
        except usb.core.USBError as usb_comm_error:
            print(f"\n Error: {print_verbose(self.target)} jumping to application command: "
                  f"{str(usb_comm_error)}.")
            sys.exit(SWITCH_APP_ERROR)

        if len(command) != bytes_to_endpoint:
            print(F"\n Error: {print_verbose(self.target)} jumping to application command: "
                  "write to endpoint size mismatch.")
            sys.exit(SWITCH_APP_ERROR)

        if not self._did_it_de_enumerate('boot'):
            print(F"\n Error: {print_verbose(self.target)} jumping to application command: "
                  "the bootloader didn't de-enumerate.")
            sys.exit(SWITCH_APP_ERROR)

        if not self._did_it_enumerate(fw_type):
            print(F"\n Error: {print_verbose(self.target)} jumping to application command: "
                  "the application didn't enumerate.")
            sys.exit(SWITCH_APP_ERROR)

    def _pre_process_app_file(self) -> Tuple[array.array, int]:
        '''
        Converts the app .hex into an array of bytes (*) \n
        Calculates the CRC32 and writes it to the last 4 bytes of the array \n
        (*) : the array needs to be of a given size - that's already taken care of \n
              in the PKOB4 .hex, but not in the CMSIS-DAP v2 .hex: hence \n
              the resulting array needs to be padded with 0xFFs
        '''
        app_file_hex = IntelHex()

        app_file_hex.fromfile(self.new_fw_file_path, format='hex')

        app_file_image = app_file_hex.tobinarray()

        if self.new_fw_type == 'cmsis':
            padding_length = APPLICATION_IMAGE_SIZE_IN_BYTES - len(
                app_file_image)
            padding = array.array('B', [0xFF] * padding_length)
            app_file_image = app_file_image + padding

        # Make sure the resulting app image byte array has the expected size
        if (len(app_file_image) != APPLICATION_IMAGE_SIZE_IN_BYTES):
            print(f"Error: {os.path.basename(self.new_fw_file_path)} has an invalid size "
                  f"({len(app_file_image)})")
            sys.exit(SWITCH_APP_ERROR)

        # Calculate the app image byte array CRC32 except the last 4 bytes
        # where the calculated CRC32 will be written
        app_file_image_crc32 = zlib.crc32(
            bytes(app_file_image[:APPLICATION_IMAGE_SIZE_IN_BYTES - 4]))

        # Make sure the value is a 32-bit unsigned integer
        app_file_image_crc32 &= 0xFFFF_FFFF

        return app_file_image, app_file_image_crc32

    def _erase_app_flash(self) -> None:
        print('\n Erasing Flash ...')

        stop_event = threading.Event()
        dot_printer_thread = threading.Thread(target=self._print_dots,
                                              args=(stop_event,))
        dot_printer_thread.start()

        command = bytearray(2)
        command[0] = commands['ERASE_FLASH']
        command[1] = commands['ERASE_APPLICATION']

        # Send command
        try:
            bytes_to_endpoint = self.usb_device.write(endpoints_numbers['COMMAND_OUT_MPLAB_FW_TYPE'],
                                                      command,
                                                      timeouts_ms['USB_COMM'])
        except usb.core.USBError as usb_comm_error:
            print(f"\n Error: {print_verbose(self.target)} erasing app Flash: "
                  f"{str(usb_comm_error)}.")
            stop_event.set()
            dot_printer_thread.join()
            sys.exit(SWITCH_APP_ERROR)

        if len(command) != bytes_to_endpoint:
            print(f"\n Error: {print_verbose(self.target)} erasing app Flash: "
                  "write to endpoint size mismatch.")
            stop_event.set()
            dot_printer_thread.join()
            sys.exit(SWITCH_APP_ERROR)

        # Check if Flash was erased w/out issues

        # Pause required between back-to-back access to USB
        time.sleep(2)

        try:
            erase_status = self.usb_device.read(endpoints_numbers['COMMAND_IN_MPLAB_BOOT'],
                                                ERASE_STATUS_SIZE_IN_BYTES,
                                                timeouts_ms['ERASE_FLASH'])
        except usb.core.USBError as usb_comm_error:
            print(f"\n Error: {print_verbose(self.target)} erasing app Flash: "
                  f"{str(usb_comm_error)}.")
            stop_event.set()
            dot_printer_thread.join()
            sys.exit(SWITCH_APP_ERROR)

        if not erase_status:
            print(f"\n Error: cannot read status from {print_verbose(self.target)} "
                  "following Flash erase.")
            stop_event.set()
            dot_printer_thread.join()
            sys.exit(SWITCH_APP_ERROR)

        if erase_status[usb_receive_offsets['COMMAND_OPCODE_ECHO']] != commands['ERASE_FLASH']:
            print("\n Error: erase status didn't echo ERASE_FLASH command.")
            stop_event.set()
            dot_printer_thread.join()
            sys.exit(SWITCH_APP_ERROR)

        error_code = erase_status[usb_receive_offsets['ERASE_FLASH_ERROR_CODE']]
        if (error_code != NO_COMMAND_ERROR):
            print(
                f"\n Error: {error_code} code erasing "
                f"{print_verbose(self.target)} Flash")
            stop_event.set()
            dot_printer_thread.join()
            sys.exit(SWITCH_APP_ERROR)

        stop_event.set()
        dot_printer_thread.join()

    def _write_a_page_to_flash(self, start_address: int, data: bytearray) -> None:
        command = bytearray(WRITE_FLASH_PAGE_COMMAND_SIZE_IN_BYTES)

        # Populate command array: opcode, start address, data # NOTE: there is an 8 bytes gap (reserved) between addr and data
        command[usb_transmit_offsets['COMMAND_OPCODE']] = commands['WRITE_PAGE']

        start_addr_as_bytes = start_address.to_bytes(
            FLASH_ADDRESS_SIZE_IN_BYTES, byteorder='little')
        command[usb_transmit_offsets['FIRST_ARGUMENT']:usb_transmit_offsets['FIRST_ARGUMENT'] +
                len(start_addr_as_bytes)] = start_addr_as_bytes

        command[usb_transmit_offsets['SECOND_ARGUMENT']:usb_transmit_offsets['SECOND_ARGUMENT'] +
                FLASH_PAGE_SIZE_IN_BYTES] = data[:FLASH_PAGE_SIZE_IN_BYTES]

        # Send command
        try:
            bytes_to_endpoint = self.usb_device.write(endpoints_numbers['COMMAND_OUT_MPLAB_BOOT'],
                                                      command,
                                                      timeouts_ms['USB_COMM'])
        except usb.core.USBError as usb_comm_error:
            print(f"\n Error: {print_verbose(self.target)} writing to Flash page: "
                  f"{str(usb_comm_error)}.")
            sys.exit(SWITCH_APP_ERROR)

        if len(command) != bytes_to_endpoint:
            print(f"\n Error: {print_verbose(self.target)} writing to Flash page: "
                  "write to endpoint size mismatch.")
            sys.exit(SWITCH_APP_ERROR)

        # Pause required between back-to-back access to USB
        time.sleep(.0125)

        try:
            write_page_status = self.usb_device.read(endpoints_numbers['COMMAND_IN_MPLAB_BOOT'],
                                                     WRITE_PAGE_STATUS_SIZE_IN_BYTES,
                                                     timeouts_ms['WRITE_FLASH_PAGE'])
        except usb.core.USBError as usb_comm_error:
            print(f"\n Error: {print_verbose(self.target)} writing to Flash page: "
                  f"{str(usb_comm_error)}.")

#            sys.exit(SWITCH_APP_ERROR) let it be caught

        if not write_page_status:
            print(f"\n Error: cannot read status from {print_verbose(self.target)} "
                  "writing to Flash page.")
            sys.exit(SWITCH_APP_ERROR)

        if write_page_status[usb_receive_offsets['COMMAND_OPCODE_ECHO']] != commands['WRITE_PAGE']:
            print("\n Error: write status didn't echo WRITE_PAGE command.")
            sys.exit(SWITCH_APP_ERROR)

        error_code = write_page_status[usb_receive_offsets['WRITE_PAGE_ERROR_CODE']]
        if (error_code != NO_COMMAND_ERROR):
            print(
                f"\n Error: {error_code} code writing "
                f"{print_verbose(self.target)} Flash page")
            sys.exit(-1)

    def _print_dots(self, stop_event: threading.Event):
        '''
        Prints dots to show that write to flash is ongoing
        '''
        while not stop_event.is_set():
            time.sleep(1)
            print(' .', end='', flush=True)

    def _write_app_flash(self, aap_file_image: array.array) -> None:
        '''
        Writes the application file into the target Flash, page by page
        '''
        print("\n\n Application being written and verified ...")

        stop_event = threading.Event()
        dot_printer_thread = threading.Thread(target=self._print_dots,
                                              args=(stop_event,))
        dot_printer_thread.start()

        data_array = bytearray(FLASH_PAGE_SIZE_IN_BYTES)

        try:
            for flash_page_start_address in range(0, len(aap_file_image), FLASH_PAGE_SIZE_IN_BYTES):
                # Write to Flash a page of aap_file_image data
                data_array = bytearray(aap_file_image[flash_page_start_address:flash_page_start_address +
                                                      FLASH_PAGE_SIZE_IN_BYTES])

                self._write_a_page_to_flash(
                    APPLICATION_START_ADDRESS + flash_page_start_address, data_array)
        except:
            stop_event.set()
            dot_printer_thread.join()
            sys.exit(SWITCH_APP_ERROR)

        stop_event.set()
        dot_printer_thread.join()

    def _get_crc32(self) -> int:
        command = bytearray(1)
        command[usb_transmit_offsets['COMMAND_OPCODE']] = commands['READ_CRC32']

        try:
            bytes_to_endpoint = self.usb_device.write(endpoints_numbers['COMMAND_OUT_MPLAB_BOOT'],
                                                      command,
                                                      timeouts_ms['READ_CRC32'])
        except usb.core.USBError as usb_comm_error:
            print(f"\n Error: {print_verbose(self.target)} reading CRC32: "
                  f"{str(usb_comm_error)}.")
            sys.exit(SWITCH_APP_ERROR)

        if len(command) != bytes_to_endpoint:
            print(f"\n Error: {print_verbose(self.target)} reading CRC32: "
                  "write to endpoint size mismatch.")
            sys.exit(SWITCH_APP_ERROR)

        # Pause required between back-to-back access to USB
        time.sleep(2)

        try:
            read_crc32_status = self.usb_device.read(endpoints_numbers['COMMAND_IN_MPLAB_BOOT'],
                                                     READ_CRC32_STATUS_SIZE_IN_BYTES,
                                                     timeouts_ms['READ_CRC32'])
        except usb.core.USBError as usb_comm_error:
            print(f"\n Error: {print_verbose(self.target)} reading CRC32: "
                  f"{str(usb_comm_error)}.")
            sys.exit(SWITCH_APP_ERROR)

        if not read_crc32_status:
            print(
                f"\n Error: cannot read CRC32 from {print_verbose(self.target)}")
            sys.exit(SWITCH_APP_ERROR)

        if read_crc32_status[usb_receive_offsets['COMMAND_OPCODE_ECHO']] != commands['READ_CRC32']:
            print(
                f"\n Error: no command echo reading "
                f"{print_verbose(self.target)} app CRC32")
            sys.exit(SWITCH_APP_ERROR)

        crc32_value = struct.unpack('<I', read_crc32_status[1:5])[0]

        return crc32_value

    def execute(self) -> None:
        '''
        Prepares the app .hex \n
        Enters bootloader mode \n
        Erases the app Flash area \n
        Writes the app to the Flash \n
        Verifies the write by double checking the CRC32
        '''
        # Convert the app .hex into an array of bytes (padded if needed) and add its CRC32
        app_file_image, app_file_image_crc32 = self._pre_process_app_file()
        crc32_as_byte_array = app_file_image_crc32.to_bytes(
            4, byteorder='little')

        for pos in range(CRC32_SIZE_IN_BYTES):
            app_file_image[APPLICATION_IMAGE_CRC_BASE_ADDRESS +
                           pos] = crc32_as_byte_array[pos]

        # Enter boot mode unless already in boot mode
        if self.current_fw_type != 'bootloader':
            self._enter_boot_mode()

        # Erase the area of Flash corresponding to the app .hex only (not the bootloader too!)
        self._erase_app_flash()

        # Write to the Flash page by page the app.hex
        self._write_app_flash(app_file_image)

        # Read the CRC32 from Flash and check it matches the one previously calculated
        crc32_value_from_flash = self._get_crc32()

        # If CRC32s match, back to app
        # If they don't, raise error (user will be offered to try switching again)
        if app_file_image_crc32 == crc32_value_from_flash:
            self._jump_to_app_mplab_boot()

        else:
            print(
                f"\n Error: CRC32 mismatch reading "
                f"{print_verbose(self.target)} Flash")
            sys.exit(SWITCH_APP_ERROR)
