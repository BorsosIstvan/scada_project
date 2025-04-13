# beweegbaar_window_object.py

class BeweegbaarWindowObject:
    def __init__(self, canvas, window_widget, window_id):
        self.canvas = canvas
        self.window_widget = window_widget  # bijv. een tk.Button of tk.Canvas
        self.window_id = window_id          # ID van create_window

        self._drag_start_x = 0
        self._drag_start_y = 0

        # Bind muisgebeurtenissen aan het widget zelf
        self.window_widget.bind("<Button-1>", self.start_slepen)
        self.window_widget.bind("<B1-Motion>", self.beweeg)

    def start_slepen(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def beweeg(self, event):
        dx = event.x - self._drag_start_x
        dy = event.y - self._drag_start_y
        self.canvas.move(self.window_id, dx, dy)
