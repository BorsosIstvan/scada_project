#  Scada object
from PIL import Image, ImageTk
import os


class ScadaObject:
    def __init__(self, canvas, x, y, width=80, height=50, color="lightblue", text="Object",
                 image_path_state_0=None, image_path_state_1=None,
                 register_type="HR", register_address=0, value=0, value_visible=False):

        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

        self.image_path_state_0 = image_path_state_0
        self.image_path_state_1 = image_path_state_1

        self.tk_image_state_0 = None
        self.tk_image_state_1 = None

        self.image_item_id = None  # komt voor canvas image
        self.image_id = None

        self.register_type = register_type
        self.register_address = register_address
        self.value = value
        self.value_visible = value_visible

        self.needs_write = False

        # Als er een afbeelding is (één van beide staten), geen rechthoek tekenen
        has_image = (self.image_path_state_0 and self.image_path_state_0.lower() != "none") or \
                    (self.image_path_state_1 and self.image_path_state_1.lower() != "none")

        fill_color = "" if has_image else self.color
        outline_color = "" if has_image else "black"

        self.rect = canvas.create_rectangle(x, y, x + width, y + height, fill=fill_color, outline=outline_color)
        self.label = canvas.create_text(x + width / 2, y + height / 2, text=text)
        self.value_label = canvas.create_text(x + width / 2, y + height + 20, text=value)

        self.load_images()  # laad beide beelden
        # Toon het juiste beeld, op basis van de waarde
        if has_image:
            image_to_use = self.tk_image_state_1 if self.value else self.tk_image_state_0
            if image_to_use:
                self.image_item_id = canvas.create_image(x, y, anchor="nw", image=image_to_use)

        self.bind_events()

    def bind_events(self):
        for item in [self.rect, self.label, self.image_item_id]:
            if item:
                self.canvas.tag_bind(item, "<Button-1>", self.on_click)
                self.canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
                self.canvas.tag_bind(item, "<ButtonRelease-1>", self.on_release)
                self.canvas.tag_bind(item, "<Double-Button-1>", self.on_double_click)
                self.canvas.tag_bind(item, "<Button-3>", self.on_right_click)

    def load_images(self):
        try:
            self.tk_image_state_0 = None
            self.tk_image_state_1 = None

            # Laad afbeelding voor state 0
            if self.image_path_state_0 and os.path.exists(self.image_path_state_0):
                image0 = Image.open(self.image_path_state_0).resize((self.width, self.height))
                self.tk_image_state_0 = ImageTk.PhotoImage(image0)

            # Laad afbeelding voor state 1
            if self.image_path_state_1 and os.path.exists(self.image_path_state_1):
                image1 = Image.open(self.image_path_state_1).resize((self.width, self.height))
                self.tk_image_state_1 = ImageTk.PhotoImage(image1)

            # Verwijder vorige image van canvas als die er is
            if self.image_item_id:
                self.canvas.delete(self.image_item_id)

            # Plaats de juiste afbeelding op canvas op basis van waarde
            image_to_use = self.tk_image_state_1 if self.value else self.tk_image_state_0
            if image_to_use:
                self.image_item_id = self.canvas.create_image(self.x, self.y, anchor="nw", image=image_to_use)

            self.bind_events()

        except Exception as e:
            print(f"Fout bij laden afbeelding: {e}")

    def on_click(self, event):
        self.offset_x = event.x - self.x
        self.offset_y = event.y - self.y
        self.click_dialog()

    def on_right_click(self, event):
        self.right_click_dialog()

    from gui.menu.dialogs.object_properties_dialog import show_properties_dialog

    def on_double_click(self, event):
        self.show_properties_dialog()

    def on_drag(self, event):
        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        dx = new_x - self.x
        dy = new_y - self.y
        self.canvas.move(self.rect, dx, dy)
        self.canvas.move(self.label, dx, dy)
        self.canvas.move(self.value_label, dx, dy)
        if self.image_item_id:
            self.canvas.move(self.image_item_id, dx, dy)
        self.x = new_x
        self.y = new_y

    def on_release(self, event):
        pass

    def serialize(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "color": self.color,
            "text": self.text,
            "image_path_state_0": self.image_path_state_0,
            "image_path_state_1": self.image_path_state_1,
            "register_type": self.register_type,
            "register_address": self.register_address,
            "value": self.value,
            "value_visible": self.value_visible
        }

    def update_visual(self):
        # Bijwerken van de coordinaten van het object:
        self.canvas.coords(self.rect, self.x, self.y, self.x + self.width, self.y + self.height)
        self.canvas.coords(self.label, self.x + self.width / 2, self.y + self.height / 2)
        self.canvas.itemconfig(self.label, text=self.text)
        self.canvas.coords(self.value_label, self.x + self.width / 2, self.y + self.height + 20)
        self.canvas.itemconfig(self.value_label, text=self.value)

        # Beeldafbeelding aanpassen op basis van de waarde (state0 / state1)
        if self.value == 0 and self.image_path_state_0 and self.image_path_state_0.lower() != "none":
            self.canvas.itemconfig(self.rect, fill="", outline="")
            self.image_path = self.image_path_state_0  # Laad de afbeelding voor state0
            self.load_images()
        elif self.value == 1 and self.image_path_state_1 and self.image_path_state_1.lower() != "none":
            self.canvas.itemconfig(self.rect, fill="", outline="")
            self.image_path = self.image_path_state_1  # Laad de afbeelding voor state1
            self.load_images()
        elif self.register_type == "HR" or self.register_type == "IR":
            self.canvas.itemconfig(self.rect, fill="", outline="")
            self.image_path = self.image_path_state_0  # Laad de afbeelding voor state0
            self.load_images()
        else:
            self.canvas.itemconfig(self.rect, fill=self.color,
                                   outline="black")  # Geen afbeelding, gewoon de kleur gebruiken

        # Correcte volgorde van lagen:
        if self.image_item_id:
            self.canvas.tag_lower(self.image_item_id)
        self.canvas.tag_raise(self.rect)
        self.canvas.tag_raise(self.label)
        self.canvas.tag_raise(self.value_label)

    def update_value(self, new_value):
        """Werk de waarde van het object bij, afhankelijk van het registertype"""
        if self.register_type in ['Co', 'DI']:  # Boolean type
            if isinstance(new_value, bool):
                self.value = new_value
            else:
                print("Waarde moet een boolean zijn voor Coils en Discrete Inputs.")
        elif self.register_type in ['IR', 'HR']:  # 16-bit integer type
            if isinstance(new_value, int) and 0 <= new_value <= 65535:
                self.value = new_value
            else:
                print("Waarde moet een 16-bit integer zijn voor Input en Holding Registers.")
        else:
            print(f"Ongeldig registertype: {self.register_type}")

    def get_value(self):
        return self.value

    def click_dialog(self):
        print("Wat wil je doen met dit object?", self.text)
        if self.register_type == "Co":
            self.value = not self.value
            self.needs_write = True

    def right_click_dialog(self):
        print("Wil je het wisselen?", self.text)