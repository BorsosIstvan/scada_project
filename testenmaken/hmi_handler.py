#  HMI functies

class HmiHandler:
    def __init__(self, canvas, tekstobject):
        self.canvas = canvas
        self.tekst = tekstobject

    def tekst_wijzigen(self):
        print("Nieuwe tekst")
        self.canvas.itemconfig(self.tekst.id, text="Status: actief")
