#  maken objectennbeweegbaar metn muis


class BeweegbaarObject:
    def __init__(self, canvas, object_id):
        self.canvas = canvas
        self.object_id = object_id
        self._drag_data = {"x": 0, "y": 0}

        self.canvas.tag_bind(self.object_id, "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(self.object_id, "<B1-Motion>", self.drag)

    def start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.canvas.move(self.object_id, dx, dy)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
