'''
Helper module: print utilities
'''


def print_verbose(target: str) -> str:
    '''
    Expands the CLI argument in more readable form
    '''
    argument_to_verbose_print = {
        'pickitbasic': "PICkit Basic",
        'evalboard': "evaluation board or kit",
        'cmsisv2': "CMSIS-DAP v2",
        'mplab': "mplab",
        'bootloader': 'bootloader',
    }

    return argument_to_verbose_print[target]
