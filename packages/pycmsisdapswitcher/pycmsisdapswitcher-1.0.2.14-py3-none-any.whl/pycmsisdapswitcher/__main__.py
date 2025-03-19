'''
pyfirmwareswitcher entry point when executed aa a module:
python3 -m pyfirmwareswitcher <args>
or executed by debugpy (see launch.json)
'''

import sys

if __name__ == "__main__":
    from .cli_parser import main as _cli_parser_main

    sys.exit(_cli_parser_main())
