'''
Fetches the tool pack for the prompted kit or tool from MCHP public pack server, \n
unzips it in a temporary directory and finds the application firmware to switch to
'''
from pathlib import Path
import zlib
import xml.etree.ElementTree
from xml.etree.ElementTree import Element
from typing import List, Optional, Tuple, Generator
from packaging.version import parse as versionparse
import contextlib
import tempfile
import shutil
import sys
import zipfile
import os

import requests
from requests.exceptions import Timeout

from .print_utils import print_verbose
from .dictionaries import toolpack_names, app_file_names

from .cache_manager import CacheManager

from .exit_codes import SERVER_ACCESS_ERROR

PACK_INDEX_NAMESPACE = 'http://packs.download.atmel.com/pack-idx-atmel-extension'

tool_pack_names = {
    'evalboard': 'PKOB4_TP',
    'pickitbasic': '',  # NOTE: to be defined (ask for it)
}

MICROCHIP_PACK_SERVER = 'https://packs.download.microchip.com'


class ToolpackServerDownloader:
    '''
    Provides methods to download the toolpack for the prompted target from MICROCHIP_PACK_SERVER \n
    to a temporary directory, find the firmware file for the prompted firmware type, save it \n
    in the cache and return the firmware file path
    '''

    @contextlib.contextmanager
    def _temporary_dir_manager(self, dir_prefix: str) -> Generator[str, None, None]:
        tmpdir = tempfile.mkdtemp(prefix=dir_prefix)
        try:
            yield tmpdir
        finally:
            shutil.rmtree(tmpdir)

    def _list_all_packs(self) -> Tuple[Optional[List[str]], Optional[Element]]:
        '''
        :return: a list of all packs on the public server, or None
        '''
        packs_index_url = MICROCHIP_PACK_SERVER + '/index.idx.gz'

        try:
            # Get from the server the packs index
            response = requests.get(packs_index_url, timeout=5)
            response.raise_for_status()

            # Decompress the server answer (.GZIP) into an XML file
            packs_index_xml = zlib.decompress(response.content,
                                              zlib.MAX_WBITS | 32)

            # Parse the XML file into an XML tree
            packs_index = xml.etree.ElementTree.fromstring(packs_index_xml)

            # Build a list of the .pdsc (pack description) elements in the tree
            packs_list = []
            for pack in packs_index.findall('./pdsc'):
                packs_list.append(pack.attrib.get(
                    f'{{{PACK_INDEX_NAMESPACE}}}name'))

            return packs_list, packs_index
        except requests.exceptions.Timeout:
            print("\n Error: unable to download the tool packs index: timeout.")
            sys.exit(SERVER_ACCESS_ERROR)
        except requests.exceptions.RequestException as e:

            print(
                f"\n Error: unable to download the tool packs index: HTTP GET exception.")
            sys.exit(SERVER_ACCESS_ERROR)

    def _get_latest_tool_pack_version(self, tool_pack_name: str, tool_packs_index: Element) -> str:
        all_tool_pack_releases = []

        for pack in tool_packs_index.findall(f'./pdsc[@atmel:name="{tool_pack_name}"]',
                                             namespaces={'atmel': PACK_INDEX_NAMESPACE}):
            for release in pack.findall('atmel:releases/atmel:release',
                                        namespaces={'atmel': PACK_INDEX_NAMESPACE}):
                all_tool_pack_releases.append({'version': release.attrib.get('version'),
                                               'description': list(release)[0].text})

        latest_version = all_tool_pack_releases[0]['version']
        for release in all_tool_pack_releases:
            if versionparse(release['version']) > versionparse(latest_version):
                latest_version = release

        return latest_version

    def _fetch_tool_pack(self, tool_pack_name: str, latest_version: str, toolpack_temp_dir_path: str) -> str:
        '''
        Downloads the requested tool pack from the Microchip packs repository into a .zip in a temporary dir
        '''

        tool_pack_url = f"{MICROCHIP_PACK_SERVER}/Microchip.{tool_pack_name}.{latest_version}.atpack"
        try:
            response = requests.get(
                tool_pack_url, allow_redirects=True, stream=True, timeout=5)
            response.raise_for_status()

            file_name = f"{toolpack_temp_dir_path}/{tool_pack_name}.{latest_version}.zip"
            with open(file_name, 'wb') as file_content:
                for chunk in response.iter_content(chunk_size=128):
                    file_content.write(chunk)

            return file_name
        except Timeout as timeout_err:
            print(
                f"\n Error: timeout accessing Microchip packs repository: "
                f"{timeout_err}")
            sys.exit(-1)
        except Exception as err:
            print(f'\n Error accessing Microchip packs repository: {err}')
            sys.exit(-1)

    def _extract_hex_save_to_cache(self, tool_pack_zip_name: str, target: str,
                                   fw_type: str, toolpack_temp_dir_path: str, tool_pack_latest_version: str) -> str:
        '''
        Extracts the app .hex from the tool pack .zip, saves it into the cache and returns the file name
        '''
        tool_pack_zip_file = zipfile.ZipFile(
            tool_pack_zip_name)  # TO DO: manage errors

        try:
            for file_name in tool_pack_zip_file.namelist():
                if os.path.basename(file_name) == app_file_names[target][fw_type]:
                    fw_zip = tool_pack_zip_file.extract(
                        file_name, path=toolpack_temp_dir_path)
                    app_file_path = os.path.join(
                        toolpack_temp_dir_path, file_name)

                    print(f"\n Application file {os.path.basename(file_name)} "
                          f"found in tool pack version {tool_pack_latest_version}")

                    cache_manager = CacheManager()
                    cache_manager.check_create_cache()
                    cache_manager.put_file(app_file_path)

                    return os.path.join(cache_manager.get_cache_dir(), os.path.basename(app_file_path))

        except KeyError:
            print(f"\n Error: {os.path.basename(file_name)} "
                  "not found in downloaded pack.")
            sys.exit(-1)

    def __init__(self, target: str, fw_type: str):
        self.target = target
        self.fw_type = fw_type

    def get_app_file_path(self) -> str:
        with self._temporary_dir_manager('toolpack_from_server') as toolpack_temp_dir_path:
            '''
            Thanks to the contextmanager call, a temporary directory is available inside  \n
            the 'with' block to download and unzip the toolpack downloaded from the server 
            '''
            app_file_path = None

            tool_packs_list, tool_packs_index = self._list_all_packs()

            tool_pack_name = toolpack_names[self.target]

            if tool_pack_name not in tool_packs_list:
                print(f"\n Error: no tool pack for {print_verbose(self.target)} "
                      "found in Microchip packs repository.")
                sys.exit(-1)

            tool_pack_latest_version = self._get_latest_tool_pack_version(
                tool_pack_name, tool_packs_index)

            tool_pack_zip_name = self._fetch_tool_pack(
                tool_pack_name, tool_pack_latest_version, toolpack_temp_dir_path)

            app_file_path = self._extract_hex_save_to_cache(
                tool_pack_zip_name, self.target, self.fw_type, toolpack_temp_dir_path, tool_pack_latest_version)

            return app_file_path
