import tkinter as tk

from testenmaken.hmi_app import HMIApp

if __name__ == "__main__":
    venster = tk.Tk()
    app = HMIApp(venster)
    venster.mainloop()
