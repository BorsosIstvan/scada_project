# gui/menu/object_properties_dialog.py
from tkinter import Toplevel, Label, Entry, Button, filedialog


def show_properties_dialog(object_manager):
    dialog = Toplevel(object_manager.canvas)
    dialog.title("Eigenschappen aanpassen")

    entries = {}
    fields = {
        "text": object_manager.text,
        "color": object_manager.color,
        "x": str(object_manager.x),
        "y": str(object_manager.y),
        "width": str(object_manager.width),
        "height": str(object_manager.height),
        "image_path_state_0": str(object_manager.image_path_state_0),
        "image_path_state_1": str(object_manager.image_path_state_1),
        "register_type": object_manager.register_type,
        "register_address": int(object_manager.register_address),
        "value": int(object_manager.value),
        "value_visible": str(object_manager.value_visible)
    }

    def browse_image_state0():
        filepath = filedialog.askopenfilename(
            filetypes=[("Afbeeldingen", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Alle bestanden", "*.*")]
        )
        if filepath:
            entries["image_path_state_0"].delete(0, 'end')
            entries["image_path_state_0"].insert(0, filepath)

    def browse_image_state1():
        filepath = filedialog.askopenfilename(
            filetypes=[("Afbeeldingen", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Alle bestanden", "*.*")]
        )
        if filepath:
            entries["image_path_state_1"].delete(0, 'end')
            entries["image_path_state_1"].insert(0, filepath)

    row = 0
    for key, value in fields.items():
        Label(dialog, text=key.capitalize()).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = Entry(dialog)
        entry.insert(0, value)
        entry.grid(row=row, column=1, padx=10, pady=5)
        entries[key] = entry
        if key == "image_path_state_0":
            Button(dialog, text="Bladeren...", command=browse_image_state0).grid(row=row, column=2, padx=5)
        elif key == "image_path_state_1":
            Button(dialog, text="Bladeren...", command=browse_image_state1).grid(row=row, column=2, padx=5)
        row += 1

    def apply_changes():
        try:
            object_manager.text = entries["text"].get()
            object_manager.color = entries["color"].get()
            object_manager.x = int(entries["x"].get())
            object_manager.y = int(entries["y"].get())
            object_manager.width = int(entries["width"].get())
            object_manager.height = int(entries["height"].get())
            object_manager.image_path_state_0 = entries["image_path_state_0"].get()
            object_manager.image_path_state_1 = entries["image_path_state_1"].get()
            object_manager.register_type = entries["register_type"].get()  # Update register type
            object_manager.register_address = entries["register_address"].get()
            object_manager.value = entries["value"].get()  # Update value
            if object_manager.register_type in ['Co', 'DI']:  # Voor boolean, converteer de waarde naar een boolean
                object_manager.value = object_manager.value.lower() == 'true'
            else:
                object_manager.value = int(object_manager.value)  # Voor HR en IR, converteer naar integer
            object_manager.value_visible = entries["value_visible"].get()
            object_manager.needs_write = True
            object_manager.update_visual()
            dialog.destroy()
        except Exception as e:
            print(f"Fout bij aanpassen: {e}")

    Button(dialog, text="Toepassen", command=apply_changes).grid(row=row, columnspan=2, pady=10)
