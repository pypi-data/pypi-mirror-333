'''
Dictionaries shared across modules
'''

vids = {
    'MCHP': 0x04D8,
    'ATMEL': 0x03EB,
}

app_pids = {
    'PICKIT_BASIC': {
        'MPLAB_BOOT_PID': 0x9057,
        'MPLAB_APP_PID': (0x9054, 0x9055, 0x9056),
        'CMSIS_V2_APP_PID': (0x90AB, 0x90AC, 0x90AD, 0x90AE)
    },
    'EVAL_BOARD': {
        'MPLAB_BOOT_PID': 0x810A,
        'MPLAB_APP_PID': (0x8109, 0x810B, 0x810C, 0x810D),
        'CMSIS_APP_PID': 0x2175,
        'CMSIS_V2_APP_PID': (0x904A, 0x904B, 0x904C, 0x904D)
    },
}

app_file_names = {
    'pickitbasic': {
        'cmsis': 'pickit_basic_app_cmsis-dap.hex',
        'mplab': 'pickit_basic_app.hex'
    },
    'evalboard': {
        'cmsis': 'pkob4_app_cmsis-dap.hex',
        'mplab': 'pkob4_app.hex'
    }
}

toolpack_names = {
    'pickitbasic': 'PICkitBasic_TP',
    'evalboard': 'PKOB4_TP'
}
