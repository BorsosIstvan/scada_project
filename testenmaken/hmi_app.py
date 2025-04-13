import tkinter as tk

from testenmaken.canvas_object import SubCanvas
from gui.menu.menu_manager import MenuManager
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE_BASE,
    WINDOW_BG_COLOR,
)
from tekst_object import Tekst
from button_object import ButtonObject
from hmi_handler import HmiHandler


class HMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{WINDOW_TITLE_BASE}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.iconbitmap("../resources/icon/scada_icon.ico")
        self.root.config(background=f"{WINDOW_BG_COLOR}")

        self.canvas = tk.Canvas(root, bg=f"{WINDOW_BG_COLOR}")
        self.canvas.pack(fill="both", expand=True)

        self.menu = MenuManager.create_menu(root)

        self.tekst = Tekst(self.canvas, 200, 200, "Hoi HMI")
        self.handler = HmiHandler(self.canvas, self.tekst)
        self.knop = ButtonObject(canvas=self.canvas, x=100, y=100, text="Knop", command=self.handler.tekst_wijzigen)
        self.sub_canvas = SubCanvas(canvas=self.canvas, parent=self.canvas, x=300, y=300)


