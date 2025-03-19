'''
Helper module to create and access the app files cache
'''


from pathlib import Path
import shutil
import os
import sys

SWITCHER_CACHE = 'cmsis_switcher_cache'


class CacheManager:
    '''
    Provides methods to create and access the app files cache
    '''

    def __init__(self):
        self.cache_dir = Path.home() / SWITCHER_CACHE

    def get_cache_dir(self) -> str:
        return Path.home() / SWITCHER_CACHE

    def check_create_cache(self) -> None:
        '''
        Checks if the cache already exists, if not creates it
        # NOTE: '/' takes care of OSes differences
        '''
        try:
            if not self.cache_dir.exists():
                self.cache_dir.mkdir(parents=True, exist_ok=True)
                print(f"\n Created cache at {self.cache_dir}.")
        except PermissionError:
            print("Permission denied: Unable to create cache directory"
                  f"at {self.cache_dir}.")
            sys.exit(-1)
        except Exception as e:
            print(
                f"An error occurred while creating cache directory: {str(e)}")
            sys.exit(-1)

    def put_file(self, src_file_path: str) -> None:
        '''
        Saves a file into the cache, replacing if a file w/ the same name exists
        '''
        dest_file = os.path.join(self.cache_dir,
                                 os.path.basename(src_file_path))

        shutil.copy2(src_file_path, dest_file)

        print(f"\n File {os.path.basename(src_file_path)} saved to cache.")

    def get_file(self, file_name: str) -> str:
        '''
        :return: the path of a given file in the cache, if it exists
                 Prints error message and sys.exit if file doesn't exist 
        '''
        if self.cache_dir.exists():
            path_in_cache = os.path.join(self.cache_dir, file_name)

            if Path(path_in_cache).is_file():
                print(f"\n File {file_name} found in cache.")
                return path_in_cache

            print(f"\n Error: file {file_name} not found in cache.")
            sys.exit(-1)

        print(f"\n Error: no cache found.")
        sys.exit(-1)
