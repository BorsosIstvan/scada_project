#  canvas in canvas voor andere objecten.
import tkinter as tk

from testenmaken.beweegbaar_window_object import BeweegbaarWindowObject


class SubCanvas:
    def __init__(self, canvas, x, y, parent, width=80, height=50, bg="white"):
        self.parent = parent
        self.sub_canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.id = canvas.create_window(x, y, window=self.sub_canvas)

        self.beweegbaar = BeweegbaarWindowObject(canvas, self.sub_canvas, self.id)


