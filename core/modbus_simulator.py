from pymodbus.client.serial import ModbusSerialClient

class ModbusSimulator:
    def __init__(self, port='COM4'):
        self.client = ModbusSerialClient(
            port=port,
            baudrate=9600,
            stopbits=1,
            bytesize=8,
            parity='N',
            timeout=1
        )
        self.client.connect()

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

    def sluit(self):
        self.client.close()

    def write_register(self, address, value):
        self.client.write_register(address, value)

    def write_coil(self, address, value):
        self.client.write_coil(address, value)
