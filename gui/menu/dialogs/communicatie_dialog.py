# menu/communicatie_dialog.py

import tkinter as tk
import serial.tools.list_ports
from core.modbus_simulator import ModbusSimulator  # pas dit aan naar jouw pad


def open_communicatie_settings(object_manager):
    print("Communicatie-instellingen openen")

    def get_available_ports():
        ports = list(serial.tools.list_ports.comports())
        return [port.device for port in ports]

    def save_settings():
        object_manager.com_port = com_port_var.get()
        object_manager.baud_rate = baud_rate_var.get()
        object_manager.modbus_enable = modbus_enable_var.get()
        object_manager.modbus.sluit()
        object_manager.modbus = ModbusSimulator(object_manager.com_port, object_manager.baud_rate)
        print(
            f"COM-poort ingesteld op {object_manager.com_port}, Baudrate: {object_manager.baud_rate}, Modbus: {object_manager.modbus_enable}")
        communicatie_dialog.destroy()

    communicatie_dialog = tk.Toplevel()
    communicatie_dialog.title("Communicatie-instellingen")

    frame = tk.Frame(communicatie_dialog)
    frame.pack(padx=10, pady=10)

    available_ports = get_available_ports()
    com_port_var = tk.StringVar(value=object_manager.com_port if object_manager.com_port in available_ports else (
        available_ports[0] if available_ports else ""))
    baud_rate_var = tk.IntVar(value=object_manager.baud_rate)
    modbus_enable_var = tk.BooleanVar(value=object_manager.modbus_enable)

    tk.Label(frame, text="Kies COM-poort:").grid(row=0, column=0, sticky="w", pady=5)
    tk.OptionMenu(frame, com_port_var, *available_ports).grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Kies Baudrate:").grid(row=1, column=0, sticky="w", pady=5)
    tk.OptionMenu(frame, baud_rate_var, 9600, 19200, 38400, 57600, 115200).grid(row=1, column=1, pady=5)

    tk.Checkbutton(frame, text="Modbus inschakelen", variable=modbus_enable_var).grid(row=2, columnspan=2, pady=5)

    tk.Button(communicatie_dialog, text="Opslaan", command=save_settings).pack(padx=10, pady=20)

    communicatie_dialog.mainloop()
