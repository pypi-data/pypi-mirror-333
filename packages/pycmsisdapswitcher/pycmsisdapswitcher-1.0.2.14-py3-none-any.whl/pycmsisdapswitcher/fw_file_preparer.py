'''
Helper module: prepares the firmware file to be loaded into target Flash
'''
from intelhex import IntelHex


class FWFilePreparer:
    '''
    Provides methods to convert the firmware file into a byte array, 
    calculate its CRC32 and append it at the end of the file 
    '''

    def __init__(self, file_path: str):
        self.file_path = file_path

    def prepare_file(self):
        # Read the firmware file in HEX format
        file_object = IntelHex()
        file_object.fromfile(self.file_path, format='hex')

        # Convert the IntelHex object into a binary array
        file_image = file_object.tobinarray()
