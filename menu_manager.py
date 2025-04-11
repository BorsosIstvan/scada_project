import tkinter as tk
from tkinter import filedialog, Menu
import json
import os


class MenuManager:
    @staticmethod
    def create_menu(root, canvas, object_manager, title_updater):
        menubar = Menu(root)
        root.config(menu=menubar)

        # Bestandsmenu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bestand", menu=file_menu)

        current_file = {"path": None}

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

        # Gereedschappen-menu
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gereedschappen", menu=tools_menu)

        def voeg_object_toe():
            object_manager.add_object(100, 100)

        tools_menu.add_command(label="Object toevoegen", command=voeg_object_toe)

        # Run-menu
        run_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=run_menu)

        def start_simulatie():
            print("Simulatie gestart (placeholder)")
            if hasattr(object_manager, "start_simulatie"):
                object_manager.start_simulatie()

        def stop_simulatie():
            print("Simulatie gestopt (placeholder)")
            if hasattr(object_manager, "stop_simulatie"):
                object_manager.stop_simulatie()

        def disable_run_menu_option(self, label):
            self.run_menu.entryconfig(label, state="disabled")

        def add_run_menu_option(self, label, command):
            self.run_menu.add_command(label=label, command=command)

        def remove_run_menu_option(self, label):
            index = self.run_menu.index(label)
            if index is not None:
                self.run_menu.delete(index)

        def enable_run_menu_option(self, label):
            self.run_menu.entryconfig(label, state="normal")

        def open_communicatie_settings():
            print("Open communicatie-instellingen (placeholder)")
            if hasattr(object_manager, "open_communication_settings"):
                object_manager.open_communication_settings()

        run_menu.add_command(label="Start simulatie", command=start_simulatie)
        run_menu.add_command(label="Stop simulatie", command=stop_simulatie)
        run_menu.add_separator()
        run_menu.add_command(label="Communicatie instellen...", command=open_communicatie_settings)

        return menubar
