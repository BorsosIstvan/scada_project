import time
import threading
from PIL import Image, ImageTk
import os
import serial.tools.list_ports
import tkinter as tk
from core.modbus_simulator import ModbusSimulator


class ScadaObject:
    def __init__(self, canvas, x, y, width=80, height=50, color="lightblue", text="Object",
                 image_path_state_0=None, image_path_state_1=None,
                 register_type="HR", register_address=0, value=0, value_visible=False):

        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

        self.image_path_state_0 = image_path_state_0
        self.image_path_state_1 = image_path_state_1

        self.tk_image_state_0 = None
        self.tk_image_state_1 = None

        self.image_item_id = None  # komt voor canvas image
        self.image_id = None

        self.register_type = register_type
        self.register_address = register_address
        self.value = value
        self.value_visible = value_visible

        self.needs_write = False

        # Als er een afbeelding is (één van beide staten), geen rechthoek tekenen
        has_image = (self.image_path_state_0 and self.image_path_state_0.lower() != "none") or \
                    (self.image_path_state_1 and self.image_path_state_1.lower() != "none")

        fill_color = "" if has_image else self.color
        outline_color = "" if has_image else "black"

        self.rect = canvas.create_rectangle(x, y, x + width, y + height, fill=fill_color, outline=outline_color)
        self.label = canvas.create_text(x + width / 2, y + height / 2, text=text)
        self.value_label = canvas.create_text(x + width / 2, y + height + 20, text=value)

        self.load_images()  # laad beide beelden
        # Toon het juiste beeld, op basis van de waarde
        if has_image:
            image_to_use = self.tk_image_state_1 if self.value else self.tk_image_state_0
            if image_to_use:
                self.image_item_id = canvas.create_image(x, y, anchor="nw", image=image_to_use)

        self.bind_events()

    def bind_events(self):
        for item in [self.rect, self.label, self.image_item_id]:
            if item:
                self.canvas.tag_bind(item, "<Button-1>", self.on_click)
                self.canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
                self.canvas.tag_bind(item, "<ButtonRelease-1>", self.on_release)
                self.canvas.tag_bind(item, "<Double-Button-1>", self.on_double_click)
                self.canvas.tag_bind(item, "<Button-3>", self.on_right_click)

    def load_images(self):
        try:
            self.tk_image_state_0 = None
            self.tk_image_state_1 = None

            # Laad afbeelding voor state 0
            if self.image_path_state_0 and os.path.exists(self.image_path_state_0):
                image0 = Image.open(self.image_path_state_0).resize((self.width, self.height))
                self.tk_image_state_0 = ImageTk.PhotoImage(image0)

            # Laad afbeelding voor state 1
            if self.image_path_state_1 and os.path.exists(self.image_path_state_1):
                image1 = Image.open(self.image_path_state_1).resize((self.width, self.height))
                self.tk_image_state_1 = ImageTk.PhotoImage(image1)

            # Verwijder vorige image van canvas als die er is
            if self.image_item_id:
                self.canvas.delete(self.image_item_id)

            # Plaats de juiste afbeelding op canvas op basis van waarde
            image_to_use = self.tk_image_state_1 if self.value else self.tk_image_state_0
            if image_to_use:
                self.image_item_id = self.canvas.create_image(self.x, self.y, anchor="nw", image=image_to_use)

            self.bind_events()

        except Exception as e:
            print(f"Fout bij laden afbeelding: {e}")

    def on_click(self, event):
        self.offset_x = event.x - self.x
        self.offset_y = event.y - self.y
        self.click_dialog()

    def on_right_click(self, event):
        self.right_click_dialog()

    def on_double_click(self, event):
        self.show_properties_dialog()

    def on_drag(self, event):
        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        dx = new_x - self.x
        dy = new_y - self.y
        self.canvas.move(self.rect, dx, dy)
        self.canvas.move(self.label, dx, dy)
        self.canvas.move(self.value_label, dx, dy)
        if self.image_item_id:
            self.canvas.move(self.image_item_id, dx, dy)
        self.x = new_x
        self.y = new_y

    def on_release(self, event):
        pass

    def serialize(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "color": self.color,
            "text": self.text,
            "image_path_state_0": self.image_path_state_0,
            "image_path_state_1": self.image_path_state_1,
            "register_type": self.register_type,
            "register_address": self.register_address,
            "value": self.value,
            "value_visible": self.value_visible
        }

    def show_properties_dialog(self):
        from tkinter import Toplevel, Label, Entry, Button, filedialog

        dialog = Toplevel(self.canvas)
        dialog.title("Eigenschappen aanpassen")

        entries = {}
        fields = {
            "text": self.text,
            "color": self.color,
            "x": str(self.x),
            "y": str(self.y),
            "width": str(self.width),
            "height": str(self.height),
            "image_path_state_0": str(self.image_path_state_0),
            "image_path_state_1": str(self.image_path_state_1),
            "register_type": self.register_type,
            "register_address": int(self.register_address),
            "value": int(self.value),
            "value_visible": str(self.value_visible)
        }

        def browse_image_state0():
            filepath = filedialog.askopenfilename(
                filetypes=[("Afbeeldingen", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Alle bestanden", "*.*")]
            )
            if filepath:
                entries["image_path_state_0"].delete(0, 'end')
                entries["image_path_state_0"].insert(0, filepath)

        def browse_image_state1():
            filepath = filedialog.askopenfilename(
                filetypes=[("Afbeeldingen", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Alle bestanden", "*.*")]
            )
            if filepath:
                entries["image_path_state_1"].delete(0, 'end')
                entries["image_path_state_1"].insert(0, filepath)

        row = 0
        for key, value in fields.items():
            Label(dialog, text=key.capitalize()).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            entry = Entry(dialog)
            entry.insert(0, value)
            entry.grid(row=row, column=1, padx=10, pady=5)
            entries[key] = entry
            if key == "image_path_state_0":
                Button(dialog, text="Bladeren...", command=browse_image_state0).grid(row=row, column=2, padx=5)
            elif key == "image_path_state_1":
                Button(dialog, text="Bladeren...", command=browse_image_state1).grid(row=row, column=2, padx=5)
            row += 1

        def apply_changes():
            try:
                self.text = entries["text"].get()
                self.color = entries["color"].get()
                self.x = int(entries["x"].get())
                self.y = int(entries["y"].get())
                self.width = int(entries["width"].get())
                self.height = int(entries["height"].get())
                self.image_path_state_0 = entries["image_path_state_0"].get()
                self.image_path_state_1 = entries["image_path_state_1"].get()
                self.register_type = entries["register_type"].get()  # Update register type
                self.register_address = entries["register_address"].get()
                self.value = entries["value"].get()  # Update value
                if self.register_type in ['Co', 'DI']:  # Voor boolean, converteer de waarde naar een boolean
                    self.value = self.value.lower() == 'true'
                else:
                    self.value = int(self.value)  # Voor HR en IR, converteer naar integer
                self.value_visible = entries["value_visible"].get()
                self.needs_write = True
                self.update_visual()
                dialog.destroy()
            except Exception as e:
                print(f"Fout bij aanpassen: {e}")

        Button(dialog, text="Toepassen", command=apply_changes).grid(row=row, columnspan=2, pady=10)

    def update_visual(self):
        # Bijwerken van de coordinaten van het object:
        self.canvas.coords(self.rect, self.x, self.y, self.x + self.width, self.y + self.height)
        self.canvas.coords(self.label, self.x + self.width / 2, self.y + self.height / 2)
        self.canvas.itemconfig(self.label, text=self.text)
        self.canvas.coords(self.value_label, self.x + self.width / 2, self.y + self.height + 20)
        self.canvas.itemconfig(self.value_label, text=self.value)

        # Beeldafbeelding aanpassen op basis van de waarde (state0 / state1)
        if self.value == 0 and self.image_path_state_0 and self.image_path_state_0.lower() != "none":
            self.canvas.itemconfig(self.rect, fill="", outline="")
            self.image_path = self.image_path_state_0  # Laad de afbeelding voor state0
            self.load_images()
        elif self.value == 1 and self.image_path_state_1 and self.image_path_state_1.lower() != "none":
            self.canvas.itemconfig(self.rect, fill="", outline="")
            self.image_path = self.image_path_state_1  # Laad de afbeelding voor state1
            self.load_images()
        elif self.register_type == "HR" or self.register_type == "IR":
            self.canvas.itemconfig(self.rect, fill="", outline="")
            self.image_path = self.image_path_state_0  # Laad de afbeelding voor state0
            self.load_images()
        else:
            self.canvas.itemconfig(self.rect, fill=self.color,
                                   outline="black")  # Geen afbeelding, gewoon de kleur gebruiken

        # Correcte volgorde van lagen:
        if self.image_item_id:
            self.canvas.tag_lower(self.image_item_id)
        self.canvas.tag_raise(self.rect)
        self.canvas.tag_raise(self.label)
        self.canvas.tag_raise(self.value_label)

    def update_value(self, new_value):
        """Werk de waarde van het object bij, afhankelijk van het registertype"""
        if self.register_type in ['Co', 'DI']:  # Boolean type
            if isinstance(new_value, bool):
                self.value = new_value
            else:
                print("Waarde moet een boolean zijn voor Coils en Discrete Inputs.")
        elif self.register_type in ['IR', 'HR']:  # 16-bit integer type
            if isinstance(new_value, int) and 0 <= new_value <= 65535:
                self.value = new_value
            else:
                print("Waarde moet een 16-bit integer zijn voor Input en Holding Registers.")
        else:
            print(f"Ongeldig registertype: {self.register_type}")

    def get_value(self):
        return self.value

    def click_dialog(self):
        print("Wat wil je doen met dit object?", self.text)
        if self.register_type == "Co":
            self.value = not self.value
            self.needs_write = True

    def right_click_dialog(self):
        print("Wil je het wisselen?", self.text)


from config import COM_PORT, BAUD_RATE, COILS, DISCRETE_INPUTS, HOLDING_REGISTERS, INPUT_REGISTERS


class ObjectManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.objects = []
        # definieer de communicatie variabelen
        self.com_port = COM_PORT
        self.baud_rate = BAUD_RATE
        self.modbus = ModbusSimulator(self.com_port)  # Zorg ervoor dat je de juiste poort kiest
        self.running = False
        self.thread = False
        self.modbus_enable = False
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
            self.running = True
            self.thread = threading.Thread(target=self._simulation_loop, daemon=True)
            self.thread.start()
            print("Simulatie gestart.")

    def stop_simulatie(self):
        """Stop de simulatie"""
        if self.running:
            self.running = False
            print("Simulatie gestopt")

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

    def open_communication_settings(self):
        print("Communicatie-instellingen openen - nog niet geïmplementeerd")

        # Dit dialoogvenster stelt de gebruiker in staat om COM-poort en baudrate te kiezen
        def get_available_ports():
            ports = list(serial.tools.list_ports.comports())
            return [port.device for port in ports]

        def save_settings():
            self.com_port = com_port_var.get()
            self.baud_rate = baud_rate_var.get()
            print(f"COM-poort ingesteld op {self.com_port}, Baudrate ingesteld op {self.baud_rate}")
            communicatie_dialog.destroy()

        communicatie_dialog = tk.Toplevel()
        communicatie_dialog.title("Communicatie-instellingen")

        # Label en dropdown voor COM-poort kiezen
        available_ports = get_available_ports()
        com_port_label = tk.Label(communicatie_dialog, text="Kies COM-poort:")
        com_port_label.pack(padx=10, pady=5, anchor="w")

        com_port_var = tk.StringVar(communicatie_dialog)

        # Zet de huidige COM-poort als de standaardwaarde (als deze is ingesteld)
        if self.com_port and self.com_port in available_ports:
            com_port_var.set(self.com_port)
        elif available_ports:
            com_port_var.set(available_ports[0])
        else:
            com_port_var.set("")  # Geen poorten beschikbaar

        com_port_dropdown = tk.OptionMenu(communicatie_dialog, com_port_var, *available_ports)
        com_port_dropdown.pack(padx=10, pady=5)

        # Label en dropdown voor baudrate kiezen
        baud_rate_label = tk.Label(communicatie_dialog, text="Kies Baudrate:")
        baud_rate_label.pack(padx=10, pady=5, anchor="w")

        baud_rate_var = tk.IntVar(communicatie_dialog)

        # Zet de huidige baudrate als de standaardwaarde
        baud_rate_var.set(self.baud_rate)  # Standaard waarde is 9600

        baud_rate_dropdown = tk.OptionMenu(communicatie_dialog, baud_rate_var, 9600, 19200, 38400, 57600, 115200)
        baud_rate_dropdown.pack(padx=10, pady=5)

        # Opslaan knop
        save_button = tk.Button(communicatie_dialog, text="Opslaan", command=save_settings)
        save_button.pack(padx=10, pady=20)

        communicatie_dialog.mainloop()
