from tkinter import Menu


def create_tools_menu(menubar, object_manager):
    tools_menu = Menu(menubar, tearoff=0)

    def voeg_object_toe():
        object_manager.add_object(100, 100)

    tools_menu.add_command(label="Object toevoegen", command=voeg_object_toe)
    menubar.add_cascade(label="Gereedschappen", menu=tools_menu)
