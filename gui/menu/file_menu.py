from tkinter import filedialog, Menu
import json
import os


def create_file_menu(root, canvas, object_manager, title_updater, menubar):
    current_file = {"path": None}
    file_menu = Menu(menubar, tearoff=0)

    def nieuw_bestand():
        object_manager.clear_objects()
        current_file["path"] = None
        title_updater("Nieuw")

    def bestand_opslaan():
        data = {
            "canvas": {"width": canvas.winfo_width(), "height": canvas.winfo_height()},
            "objects": object_manager.serialize_objects()
        }
        if not current_file["path"]:
            pad = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("SCADA Bestanden", "*.json")])
            if not pad:
                return
            current_file["path"] = pad

        with open(current_file["path"], "w") as f:
            json.dump(data, f, indent=4)
        title_updater(os.path.basename(current_file["path"]))

    def bestand_opslaan_als():
        data = {
            "canvas": {"width": canvas.winfo_width(), "height": canvas.winfo_height()},
            "objects": object_manager.serialize_objects()
        }
        pad = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("SCADA Bestanden", "*.json")])
        if not pad:
            return
        current_file["path"] = pad
        with open(current_file["path"], "w") as f:
            json.dump(data, f, indent=4)
        title_updater(os.path.basename(current_file["path"]))

    def bestand_openen():
        pad = filedialog.askopenfilename(filetypes=[("SCADA Bestanden", "*.json")])
        if not pad:
            return
        try:
            with open(pad, "r") as f:
                data = json.load(f)
            object_manager.clear_objects()
            object_manager.load_from_data(data["objects"])
            current_file["path"] = pad
            title_updater(os.path.basename(pad))
        except Exception as e:
            print("Fout bij laden:", e)

    file_menu.add_command(label="Nieuw", command=nieuw_bestand)
    file_menu.add_command(label="Openen", command=bestand_openen)
    file_menu.add_command(label="Opslaan", command=bestand_opslaan)
    file_menu.add_command(label="Opslaan als", command=bestand_opslaan_als)
    file_menu.add_separator()
    file_menu.add_command(label="Afsluiten", command=root.quit)

    menubar.add_cascade(label="Bestand", menu=file_menu)
