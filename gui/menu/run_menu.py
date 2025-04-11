from tkinter import Menu
from gui.menu.dialogs.communicatie_dialog import open_communicatie_settings as communicatie_dialoog



def create_run_menu(menubar, object_manager):
    run_menu = Menu(menubar, tearoff=0)

    def start_simulatie():
        print("Simulatie gestart")
        if hasattr(simulatie_manager, "start_simulatie"):
            object_manager.start_simulatie()

    def stop_simulatie():
        print("Simulatie gestopt")
        if hasattr(simulatie_manager, "stop_simulatie"):
            simulatie_manager.stop_simulatie()

    def open_communicatie_settings():
        communicatie_dialoog(object_manager)

    run_menu.add_command(label="Start simulatie", command=start_simulatie)
    run_menu.add_command(label="Stop simulatie", command=stop_simulatie)
    run_menu.add_separator()
    run_menu.add_command(label="Communicatie instellen...", command=open_communicatie_settings)

    menubar.add_cascade(label="Run", menu=run_menu)
