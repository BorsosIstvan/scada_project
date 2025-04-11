# SCADA app main.py
import tkinter as tk
from managers.object_manager import ObjectManager
from managers.simulatie_manager import SimulatieManager
from gui.menu.menu_manager import MenuManager
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE_BASE, WINDOW_BG_COLOR
)


class SCADAApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.title(f"{WINDOW_TITLE_BASE} - Nieuw")

        self.canvas = tk.Canvas(root, bg=WINDOW_BG_COLOR)
        self.canvas.pack(fill="both", expand=True)

        self.current_name = "Nieuw"

        def set_name(name):
            self.current_name = name
            update_title()

        def update_title():
            status = ""
            if self.object_manager.running:
                status += " | Simulatie actief"
            if self.object_manager.modbus_enable:
                if self.object_manager.modbus and self.object_manager.modbus.client and self.object_manager.modbus.client.connected:
                    status += " | Modbus OK"
                else:
                    status += " | Modbus geen verbinding"
            else:
                status += " | Modbus uitgeschakeld"

            self.root.title(f"{WINDOW_TITLE_BASE} - {self.current_name}{status}")

        self.object_manager = ObjectManager(self.canvas, update_title)
        self.simulatie_manager = SimulatieManager(self.canvas, update_title)
        self.menu = MenuManager.create_menu(root, self.canvas, self.object_manager, set_name)


if __name__ == "__main__":
    root = tk.Tk()
    app = SCADAApp(root)
    root.mainloop()
