from pymodbus.client.serial import ModbusSerialClient
from config import MODBUS_CONFIG


class ModbusSimulator:
    def __init__(self, port=None, baudrate=None):
        # Gebruik de waarden uit de config of fallback naar default
        self.port = port or MODBUS_CONFIG["com_port"]
        self.baudrate = baudrate or MODBUS_CONFIG["baud_rate"]
        self.stopbits = MODBUS_CONFIG["stopbits"]
        self.bytesize = MODBUS_CONFIG["bytesize"]
        self.parity = MODBUS_CONFIG["parity"]
        self.timeout = MODBUS_CONFIG["timeout"]
        # Initialiseer de client met de configuratie
        self.client = ModbusSerialClient(
            port=self.port,
            baudrate=self.baudrate,
            stopbits=self.stopbits,
            bytesize=self.bytesize,
            parity=self.parity,
            timeout=self.timeout
        )

    def lees_register(self, register_type, register_address):
        if register_type == 'holding_register':
            result = self.client.read_holding_registers(address=register_address, count=1)
            if not result.isError():
                return result.registers[0]
        elif register_type == 'coil':
            result = self.client.read_coils(address=register_address, count=1)
            if not result.isError():
                return result.bits[0]
        return None

    def connect(self):
        self.client.connect()

    def sluit(self):
        self.client.close()

    def write_register(self, address, value):
        self.client.write_register(address, value)

    def write_coil(self, address, value):
        self.client.write_coil(address, value)
