#  Knop object
import tkinter as tk

from testenmaken.beweegbaar_window_object import BeweegbaarWindowObject


class ButtonObject:
    def __init__(self, canvas, x, y, text, command=None):
        self.canvas = canvas
        self.command = command
        self.button = tk.Button(canvas, text=text, command=command)
        self.id = canvas.create_window(x, y, window=self.button)

        self.beweegbaar = BeweegbaarWindowObject(canvas, self.button, self.id)
