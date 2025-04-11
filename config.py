# config.py


# Venster instellingen
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE_BASE = "SCADA Editor"
WINDOW_BG_COLOR = "orange"


# Communicatie instellingen
COM_PORT = "COM4"
BAUD_RATE = 9600

# Modbus register instellingen
COILS = [False] * 4
DISCRETE_INPUTS = [False] * 1
HOLDING_REGISTERS = [0] * 3
INPUT_REGISTERS = [0] * 1

# Modbus instellingen
MODBUS_CONFIG = {
    'com_port': 'COM4',        # Standaard COM-poort
    'baud_rate': 9600,         # Standaard baud rate
    'stopbits': 1,             # Stopbits
    'bytesize': 8,             # Bytegrootte
    'parity': 'N',             # Pariteit
    'timeout': 1               # Timeout in seconden
}
MODBUS_ENABLE = True
