import time
import threading
from core.modbus_simulator import ModbusSimulator
from config import MODBUS_ENABLE_DEFAULT  # Importeer de waarde uit config.py
from config import COM_PORT, BAUD_RATE, COILS, DISCRETE_INPUTS, HOLDING_REGISTERS, INPUT_REGISTERS
from gui.objecten.scada_object import ScadaObject


class ObjectManager:
    def __init__(self, canvas, update_title_callback):
        self.canvas = canvas
        self.objects = []
        self.update_title_callback = update_title_callback
        # definieer de communicatie
        self.com_port = COM_PORT
        self.baud_rate = BAUD_RATE
        self.modbus = ModbusSimulator(self.com_port, self.baud_rate)  # Zorg ervoor dat je de juiste poort kiest
        # self.modbus.connect()
        self.running = False
        self.thread = False
        self.modbus_enable = MODBUS_ENABLE_DEFAULT
        # definieer de Modbus registerstructuur
        self.coils = COILS  # [False] * 4  # Co (uitgangen)
        self.discrete_inputs = DISCRETE_INPUTS  # [False] * 1  # DI (ingangen)
        self.holding_registers = HOLDING_REGISTERS  # [0] * 3  # HR (uitgangen)
        self.input_registers = INPUT_REGISTERS  # [0] * 1  # IR (ingangen)

    def add_object(self, x, y):
        obj = ScadaObject(self.canvas, x, y)
        self.objects.append(obj)

    def clear_objects(self):
        for obj in self.objects:
            self.canvas.delete(obj.rect)
            self.canvas.delete(obj.label)
            self.canvas.delete(obj.value_label)
            self.canvas.delete(obj.image_item_id)
        self.objects = []

    def serialize_objects(self):
        return [obj.serialize() for obj in self.objects]

    def load_from_data(self, data_list):
        self.clear_objects()
        for data in data_list:
            obj = ScadaObject(
                self.canvas,
                data["x"],
                data["y"],
                data.get("width", 80),
                data.get("height", 50),
                data.get("color", "lightblue"),
                data.get("text", "Object"),
                data.get("image_path_state_0", "None"),
                data.get("image_path_state_1", "None"),
                data.get("register_type", "HR"),
                data.get("register_address", 0),
                data.get("value", "100"),
                data.get("value_visible", False)
            )
            self.objects.append(obj)

    def start_simulatie(self):
        """Start de simulatie in een aparte thread"""
        if not self.running:
            if self.modbus_enable:
                self.modbus.connect()
            self.running = True
            self.thread = threading.Thread(target=self._simulation_loop, daemon=True)
            self.thread.start()
            print("Simulatie gestart.")
            self.update_title_callback()

    def stop_simulatie(self):
        """Stop de simulatie"""
        if self.running:
            self.running = False
            self.modbus.sluit()
            print("Simulatie gestopt")
            self.update_title_callback()

    def _simulation_loop(self):
        while self.running:
            # 0. Schrijft in register
            for obj in self.objects:
                if obj.needs_write:
                    print("Write register of coil naar plc")
                    self.write_registers(obj)
                    obj.needs_write = False  # Reset flag
            # 1. Lees van Modbus en update registers
            for i in range(len(self.holding_registers)):
                val = self.modbus.lees_register("holding_register", i)
                if val is not None:
                    self.holding_registers[i] = val

            for i in range(len(self.input_registers)):
                val = self.modbus.lees_register("input_register", i)
                if val is not None:
                    self.input_registers[i] = val

            for i in range(len(self.coils)):
                val = self.modbus.lees_register("coil", i)
                if val is not None:
                    self.coils[i] = val

            for i in range(len(self.discrete_inputs)):
                val = self.modbus.lees_register("discrete_input", i)
                if val is not None:
                    self.discrete_inputs[i] = val
            # 2. Synchroniseer objectwaarden
            for obj in self.objects:
                try:
                    addr = int(obj.register_address)
                    if obj.register_type == "HR":
                        obj.value = self.holding_registers[addr]
                    elif obj.register_type == "IR":
                        obj.value = self.input_registers[addr]
                    elif obj.register_type == "Co":
                        obj.value = self.coils[addr]
                    elif obj.register_type == "DI":
                        obj.value = self.discrete_inputs[addr]
                    obj.update_visual()
                except Exception as e:
                    print("Fout bij update object:", e)

            time.sleep(1)

    def write_registers(self, obj):
        if obj.register_type == "HR":
            self.modbus.write_register(int(obj.register_address), int(obj.value))
        elif obj.register_type == "Co":
            self.modbus.write_coil(int(obj.register_address), bool(obj.value))

    def write_object_to_plc(self, obj):
        try:
            address = int(obj.register_address)
            value = int(obj.value)  # Zorg dat het een integer is

            if obj.register_type == "HR":
                self.modbus.write_register(address, value)
            elif obj.register_type == "Co":
                self.modbus.write_coil(address, bool(value))
            else:
                print(f"Schrijven van type {obj.register_type} niet ondersteund.")
        except Exception as e:
            print("Fout bij schrijven naar PLC:", e)
