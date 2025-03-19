'''
Main module of the pycmsisdapswitcher: gets things done
'''
import sys
from pathlib import Path
import logging
import platform
from typing import Dict
import usb.core
import usb.util
import usb.backend.libusb1

from pycmsisdapswitcher import dictionaries
from .fw_file_fetcher import FWFileFetcher
from .fw_file_loader import FWFileLoader
from .print_utils import print_verbose
from .exit_codes import SERVER_ACCESS_ERROR, SWITCH_APP_ERROR


def get_libusb_backend():
    """
    Select and return the appropriate libusb backend based on the operating system and machine architecture.

    :returns: The appropriate libusb backend for the current platform.
    :rtype: usb.backend.libusb1.Libusb1Backend or None

    The function performs the following checks to determine the correct backend:

    - **Windows**:
      - If the machine architecture is `64bit`, it uses the `libusb-1.0.dll` located in the `libusb/win64` directory relative to the script's location.
      - If the machine architecture is `32bit`, it uses the `libusb-1.0.dll` located in the `libusb/win32` directory relative to the script's location.
      - For other architectures, it will attempt to get a backend through pyusb by searching in default OS locations.

    - **Linux**:
      -  It will attempt to get a backend through pyusb by searching in default OS locations.

    - **Darwin (macOS)**:
      - If the machine architecture is `arm64`, it uses the `libusb-1.0.dylib` located in the `libusb/darwin-arm64` directory relative to the script's location.
      - If the machine architecture is `x86_64`, it uses the `libusb-1.0.dylib` located in the `libusb/darwin-x86_64` directory relative to the script's location.
      - For other architectures, it will attempt to get a backend through pyusb by searching in default OS locations..

    - **Other Operating Systems**:
      - It will attempt to get a backend through pyusb by searching in default OS locations.
    """
    backend = None
    if platform.system() == "Windows":
        arch = platform.architecture()[0]
        if arch == "64bit":
            libusb_path = str(
                (Path(__file__).parent / "libusb/win64/libusb-1.0.dll").resolve())
            backend = usb.backend.libusb1.get_backend(
                find_library=lambda x: libusb_path)
        else:
            libusb_path = str(
                (Path(__file__).parent / "libusb/win32/libusb-1.0.dll").resolve())
            backend = usb.backend.libusb1.get_backend(
                find_library=lambda x: libusb_path)
    elif platform.system() == "Linux":
        backend = usb.backend.libusb1.get_backend()
    elif platform.system() == "Darwin":
        if platform.machine() == "arm64":
            libusb_path = str(
                (Path(__file__).parent / "libusb/darwin-arm64/libusb-1.0.dylib").resolve())
            backend = usb.backend.libusb1.get_backend(
                find_library=lambda x: libusb_path)
        elif platform.machine() == "x86_64":
            libusb_path = str(
                (Path(__file__).parent / "libusb/darwin-x86_64/libusb-1.0.dylib").resolve())
            backend = usb.backend.libusb1.get_backend(
                find_library=lambda x: libusb_path)
        else:
            backend = usb.backend.libusb1.get_backend()
    else:
        backend = usb.backend.libusb1.get_backend()
    return backend


def set_pyusb_logging_level(level=logging.DEBUG):
    # Configure logging for the 'usb' module
    logging.basicConfig(level=level)
    logger = logging.getLogger('usb')
    logger.setLevel(level)

    # Create a console handler and set the level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)
    logger_backend = logging.getLogger('usb.backend')
    logger_backend.setLevel(level)


def _find_device(target: str) -> tuple[usb.core.Device, str]:
    backend = get_libusb_backend()
    if backend == None:
        print("ERROR: No libusb backend found")
        sys.exit(-1)
    if target == 'evalboard':
        target_key = "EVAL_BOARD"
    else:
        target_key = "PICKIT_BASIC"

    # First look for one (and only one) target in application mode
    usb_device_mplab = []
    for pid in dictionaries.app_pids[target_key]["MPLAB_APP_PID"]:
        usb_device_mplab.extend(list(usb.core.find(
            idVendor=dictionaries.vids['MCHP'],
            idProduct=pid,
            find_all=True,
            backend=backend)))

    usb_device_cmsis2 = []
    for pid in dictionaries.app_pids[target_key]["CMSIS_V2_APP_PID"]:
        usb_device_cmsis2.extend(list(usb.core.find(
            idVendor=dictionaries.vids['MCHP'],
            idProduct=pid,
            find_all=True,
            backend=backend)))

    if len(usb_device_mplab) + len(usb_device_cmsis2) > 1:
        print(f"\n Error: more than one {print_verbose(target)} found. \n"
              "Please only have one target plugged in.")
        sys.exit(-1)

    if len(usb_device_mplab) == 1:
        usb_device = usb_device_mplab[0]
        fw_type = 'mplab'
        return usb_device, fw_type

    if len(usb_device_cmsis2) == 1:
        usb_device = usb_device_cmsis2[0]
        fw_type = 'cmsisv2'
        return usb_device, fw_type

    # Then check if there could an nEDBG board actually plugged in
    usb_device_cmsis = list(
        usb.core.find(idVendor=dictionaries.vids['ATMEL'],
                      idProduct=dictionaries.app_pids["EVAL_BOARD"]["CMSIS_APP_PID"],
                      find_all=True,
                      backend=backend))
    if len(usb_device_cmsis) > 0:
        print(f"\n The {print_verbose(target)} plugged in "
              "already supports CMSIS-DAP (v1).")
        sys.exit(-1)

    # Then check if there could be one (and only one) target in bootloader mode,
    # e.g. because a previous app switch failed leaving the target in boot
    usb_device_boot = []
    usb_device_boot.extend(list(usb.core.find(
        idVendor=dictionaries.vids['MCHP'],
        idProduct=dictionaries.app_pids[target_key]["MPLAB_BOOT_PID"],
        find_all=True,
        backend=backend)))

    if len(usb_device_boot) > 1:
        print(f"\n Error: more than one {print_verbose(target)} found. \n"
              "Please only have one target plugged in.")
        sys.exit(-1)

    if len(usb_device_boot) == 1:
        usb_device = usb_device_boot[0]
        fw_type = 'bootloader'
        return usb_device, fw_type

    # Nothing could be found
    print(f"\n Error: no {print_verbose(target)} found.")
    sys.exit(-1)


def _get_yes_or_no_answer(prompt: str) -> str:
    answer = None

    while not answer:
        answer = input(prompt).strip().lower()
        if answer not in ['y', 'n']:
            print("\n Error: please enter 'y' for yes or 'n' for no.")
            answer = None

    return answer


def main(arguments: Dict) -> None:
    '''
    Processes the arguments from the CLI to perform the firmware switch.

    Catches the exceptions and prints related error messages before terminating the switcher.
    '''
    try:
        from . import __version__
    except ImportError:
        __version__ = "1.0.0"

    print(f"\n *** Microchip pycmsisdapswitcher firmware switcher "
          f"version {__version__} started ***")

    target = arguments['<target>']
    fw_source = arguments['--source']
    fw_type = arguments['--fwtype']

    # Some error conditions might trigger executing again the switcher
    continue_looping = True
    while continue_looping:
        try:
            usb_device, current_fw_type = _find_device(target)

            print(f"\n Found {print_verbose(target)} S/N {usb_device.serial_number} "
                  f"running {print_verbose(current_fw_type)} application.")

            fw_file_fetcher = FWFileFetcher(target, fw_source, fw_type)
            fw_file_path = fw_file_fetcher.fetch_fw_file()

            loader = FWFileLoader(target,
                                  usb_device,
                                  current_fw_type,
                                  new_fw_file_path=fw_file_path,
                                  new_fw_type=fw_type)

            loader.execute()

            continue_looping = False

            print("\n\n Application switch completed.")

        except SystemExit as sys_ex:
            exit_reason = sys_ex.code
            if exit_reason == SERVER_ACCESS_ERROR:
                answer = _get_yes_or_no_answer(
                    "\n Couldn't access the packs server. Try cache instead? (y/n): ")
                if answer == 'y':
                    fw_source = 'cache'
                else:
                    print("\n Microchip pycmsisdapswitcher operation user terminated.")
                    sys.exit(-1)
            elif exit_reason == SWITCH_APP_ERROR:
                answer = _get_yes_or_no_answer(
                    "\n Failed to switch application. Try again? (y/n): ")
                if answer == 'n':
                    print("\n Microchip pycmsisdapswitcher operation user terminated.")
                    sys.exit(-1)
            else:
                print("\n Microchip pycmsisdapswitcher operation couldn't be completed.")
                sys.exit(-1)
        except ValueError as ve:
            if platform.system == "Linux":
                print("\n Linux udev settings required: please see README.")
            else:
                print(f"Error: {str(ve)}")
            sys.exit(-1)
