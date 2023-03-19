import tkinter
import tkinter as tk
from tkinter import ttk


class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("NetScanner - Prototype")
        self.frame = ttk.Frame(self)
        self.frame.pack()

        host_info_frame = tkinter.LabelFrame(self.frame, text="Host Information")
        host_info_frame.grid(row=0, column=0, padx=20, pady=20)

        lblHostname = tkinter.Label(host_info_frame, text="Name:")
        lblHostname.grid(row=0, column=0)

        lblHostnameValue = tkinter.Label(host_info_frame, text="xxxx")
        lblHostnameValue.grid(row=0, column=2)

        lblHostOS = tkinter.Label(host_info_frame, text="OS:")
        lblHostOS.grid(row=0, column=3)

        lblHostOSValue = tkinter.Label(host_info_frame, text="xxxx")
        lblHostOSValue.grid(row=0, column=4)


if __name__ == "__main__":
    window = Window()
    window.mainloop()