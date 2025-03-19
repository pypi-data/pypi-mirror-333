'''
pycmsisdapswitcher

Usage:
  pycmsisdapswitcher <target> [--source=<source>] [--fwtype=<fw_type>] [--version]

Options:
  -h --help     Show this screen
  --version     Show version
  --source=<source>   Specifies the source of the firmware (default: server)
                      Currently supported values:
                        server (firmware downloaded from https://packs.download.microchip.com/)
                        <firmware file name with relative or absolute path>
                        cache (firmware retrieved from the internal ~/cmsis_switcher_cache directory)
  --fwtype=<fw_type>  Specifies the firmware type
                      Currently supported values:
                        mplab (MCHP proprietary firmware)
                        cmsis (ARM standard CMSIS-DAP v2 implementation)

  Currently supported values for <target>:
    pickitbasic
    evalboard

'''

import sys
from docopt import docopt
from .switcher_main import main as _switcher_main

PY_FW_SWITCHER_VERSION = '1.0.0'


def main() -> None:
    '''
    Gets the CLI arguments and converts them to lowercase  \n
    If valid arguments, passes them to _app_switcher_main \n
    if invalid arguments, prints error message and sys.exit(-1)
    '''
    try:
        from . import __version__
    except ImportError:
        __version__ = "1.0.0"

    arguments = docopt(__doc__, version=__version__)

    for key, value in arguments.items():
        if isinstance(value, str):
            arguments[key] = value.lower()

    if not arguments['--source']:
        # MCHP public tool packs server is the default source
        arguments['--source'] = 'server'

    if arguments['--source'] in ['server', 'cache'] and not arguments['--fwtype']:
        # CMSIS v2 is the default firmware type for server or cache
        arguments['--fwtype'] = 'cmsis'

    if arguments['<target>'] in ['pickitbasic', 'evalboard']:
        _switcher_main(arguments)
    else:
        print(f"Error: {arguments['<target>']} unsupported.")
        sys.exit(-1)


if __name__ == '__main__':
    sys.exit(main())
