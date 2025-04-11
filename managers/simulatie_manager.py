import threading
import time


class SimulatieManager:
    def __init__(self, modbus, update_title_callback):
        self.modbus = modbus
        self.update_title_callback = update_title_callback
        self.running = False
        self.thread = None
        self.stop_event = threading.Event()

    def start_simulatie(self):
        if not self.running:
            if self.modbus:
                self.modbus.connect()
            self.running = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.loop, daemon=True)
            self.thread.start()
            print("Simulatie gestart.")
            self.update_title_callback()
            self.loop()

    def stop_simulatie(self):
        if self.running:
            self.running = False
            self.stop_event.set()
            if self.modbus:
                self.modbus.sluit()
            print("Simulatie gestopt")
            self.update_title_callback()

    def loop(self):
        print("loop werkt")

    def _simulation_loop(self):
        print("_simulation_loop gestart")
        try:
            while not self.stop_event.is_set():
                # Hier kan je logica toevoegen voor het simuleren of uitlezen van objecten
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
        except Exception as e:
            print(f"FOUT in _simulation_loop: {e}")
