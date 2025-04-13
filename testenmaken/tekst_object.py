# Teks object
from testenmaken.bewegbaar_object import BeweegbaarObject


class Tekst:
    def __init__(self, canvas, x, y, text):
        self.canvas = canvas
        self.text = text
        self.id = self.canvas.create_text(x, y, text=self.text, fill="black", font=("Arial", 16))

        # Maak het object beweegbaar
        self.beweegbaar = BeweegbaarObject(self.canvas, self.id)
