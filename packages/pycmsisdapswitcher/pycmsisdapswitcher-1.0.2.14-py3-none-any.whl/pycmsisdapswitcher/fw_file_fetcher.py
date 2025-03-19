'''
Helper module: based on the CLI arguments, gets the new firmware file path
'''
import os
import sys
from .toolpack_server_downloader import ToolpackServerDownloader
from .cache_manager import CacheManager
from .dictionaries import app_file_names


class FWFileFetcher:
    '''
    Provides methods to get the new firmware file path
    '''

    def __init__(self, target: str, fw_source: str, fw_type: str):
        self.target = target
        self.fw_source = fw_source
        self.fw_type = fw_type

    def fetch_fw_file(self) -> str:
        '''
        Gets the new firmware file path

        :return: the (absolute) path to the file, if found

        Prints error message and sys.exit(-1) if file not found 
        '''
        file_path = None

        if '.hex' in self.fw_source:
            if os.path.isabs(self.fw_source):
                file_path = self.fw_source
            else:
                file_path = os.path.join(os.getcwd(), self.fw_source)

            if os.path.exists(self.fw_source):
                print(f"\n New firmware file at {file_path} located.")
                return file_path

            print(
                f"\n Error: new firmware file {self.fw_source} not found in {os.getcwd()}.")
            sys.exit(-1)
        else:
            if 'server' in self.fw_source:
                toolpack_server_downloader = ToolpackServerDownloader(
                    target=self.target, fw_type=self.fw_type)

                file_path = toolpack_server_downloader.get_app_file_path()
            else:
                if 'cache' in self.fw_source:
                    cache = CacheManager()

                    return cache.get_file(file_name=app_file_names[self.target][self.fw_type])

        return file_path
