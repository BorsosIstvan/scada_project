#  Hoofdmenu-manager
from tkinter import Menu
from .file_menu import create_file_menu
from .tools_menu import create_tools_menu
from .run_menu import create_run_menu


class MenuManager:
    @staticmethod
    def create_menu(root, canvas=None, object_manager=None, title_updater=None):
        menubar = Menu(root)
        root.config(menu=menubar)

        create_file_menu(root, canvas, object_manager, title_updater, menubar)
        create_tools_menu(menubar, object_manager)
        create_run_menu(menubar, object_manager)

        return menubar
