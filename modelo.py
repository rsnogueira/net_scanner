import tkinter as tk
from tkinter import *
import os


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Command Resolver")
        self.geometry("720x550")
        self.resizable(False, False)
        self.iconphoto(False, tk.PhotoImage(file="img/title_icon.png"))

        ## Creating a container
        container = tk.Frame(self, bg="#8AA7A9")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        ## Initialize Frames
        self.frames = {}
        self.HomePage = HomePage
        self.Validation = Validation

        ## Defining Frames and Packing it
        for F in {HomePage, Validation}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        menubar = frame.create_menubar(self)
        self.configure(menu=menubar)
        frame.tkraise()


#---------------------------------------- HOME PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class HomePage(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Command Resolver", font=('Arial', '18'))
        label.pack(pady=0,padx=0)

        ## ADD CODE HERE TO DESIGN THIS PAGE

        lbl1 = tk.Label(self, text="Comando: ")
        lbl1.place(x=10, y=40)

        self.txtCommand = Entry(self, width=90)
        self.txtCommand.place(x=73, y=40)

        self.btnExec = Button(self, text="Executar", width=10, command=lambda: self.enviarComando())
        self.btnExec.place(x=630, y=35)

        self.txtArea = Text(self, width=87, height=27, bg="#b8bacc", state="disabled")
        self.txtArea.place(x=10,y=70)

    def enviarComando(self):
        cmd = self.txtCommand.get()
        result = os.popen(cmd).read()
        self.txtArea.configure(state="normal")
        self.txtArea.delete("1.0", END)
        self.txtArea.insert(END, "Comando executado: {0}\n\n".format(cmd))
        self.txtCommand.delete(0, END)
        self.txtArea.insert(END, result)
        self.txtArea.configure(state="disabled")

    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Project", command=lambda: parent.show_frame(parent.Validation))
        filemenu.add_command(label="Close", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)

        ## proccessing menu
        processing_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Validation", menu=processing_menu)
        processing_menu.add_command(label="validate")
        processing_menu.add_separator()

        ## help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")
        help_menu.add_separator()

        return menubar

#---------------------------------------- Validation PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class Validation(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Validation Page", font=('Times', '20'))
        label.pack(pady=0,padx=0)

        ## ADD CODE HERE TO DESIGN THIS PAGE

    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Project", command=lambda: parent.show_frame(parent.Validation))
        filemenu.add_command(label="Close", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)

        ## proccessing menu
        processing_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Validation", menu=processing_menu)
        processing_menu.add_command(label="validate")
        processing_menu.add_separator()

        ## help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")
        help_menu.add_separator()

        return menubar

if __name__ == "__main__":
    app = App()
    app.mainloop()
