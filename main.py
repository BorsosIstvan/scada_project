# SCADA app main.py
import tkinter as tk
from object_manager import ObjectManager
from menu_manager import MenuManager


class SCADAApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("SCADA Editor - Nieuw")

        self.canvas = tk.Canvas(root, bg="orange")
        self.canvas.pack(fill="both", expand=True)

        self.object_manager = ObjectManager(self.canvas)

        def update_title(name):
            self.root.title(f"SCADA Editor - {name}")

        self.menu = MenuManager.create_menu(root, self.canvas, self.object_manager, update_title)


if __name__ == "__main__":
    root = tk.Tk()
    app = SCADAApp(root)
    root.mainloop()
