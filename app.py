import ipaddress
import threading
import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter.constants import END

from host import Host
from localhost import Localhost
from discovery import Discovery


class App:

    def __init__(self, root):
        self.root = root
        self.active_hosts = []
        self.hidden = 0
        self.root.title("NetScanner - Prototype")
        self.root.iconphoto(False, tkinter.PhotoImage(file="img/title_icon.png"))
        # window.geometry("720x550")
        self.root.resizable(False, False)
        self.frame = tkinter.Frame(self.root)
        # self.frame.pack(side="left", fill=tkinter.BOTH, expand=1)
        self.host = Localhost()
        self.home()
        # self.show_active_hosts()


    def sweep_action(self):

        selected_network = self.combo_interfaces.get()
        if selected_network == '':
            messagebox.showerror("::Error Message::", "Please, choose one network to scan!")
        else:
            varredura = Discovery()
            net = ipaddress.IPv4Network(selected_network)  # nao apagar
            my_ip = self.host.get_ip_by_network(selected_network)
            varredura.network_scan(my_ip, net)  # nao apagar
            # self.progress_frame.destroy()
            # varredura.port_scan('192.168.0.110')
            self.active_hosts = sorted(varredura.get_active_hosts(), key=ipaddress.IPv4Address)  # nao apagar
            if len(self.active_hosts) > 0:
                self.show_active_hosts()
                # for item in self.active_hosts:
                #     self.listBox.insert(tkinter.END, item)

    def find_ports_action(self):
        # print(self.listBox.keys())
        if self.listBox.size() == 0:
            messagebox.showerror("::Error Message::", "Please, choose one IP to scan!")
            return ""

        for i in self.listBox.curselection():
            host = Host(self.listBox.get(i))

        host.port_scan()
        self.txtArea.configure(state="normal")
        self.txtArea.delete("1.0", END)
        self.txtArea.insert(END, host.getAvailableServices())
        self.txtArea.configure(state="disabled")
        #     print(f"IP: {ip}\n{}")
        # messagebox.showerror("::Error Message::", f"{self.listBox.get(i)}")



    def home(self):

        self.host_info_frame = tkinter.LabelFrame(self.root, text="Host Information")
        # self.host_info_frame.pack(side = "left", fill = tkinter.BOTH, expand = 1)
        self.host_info_frame.grid(row=0, column=0, padx=20, pady=3)

        self.lblHostname = tkinter.Label(self.host_info_frame, text=f"Name:")
        self.lblHostname.grid(row=0, column=0)

        self.lblHostnameValue = tkinter.Label(self.host_info_frame, text=self.host.get_hostname())
        self.lblHostnameValue.grid(row=0, column=1)

        self.lblHostOS = tkinter.Label(self.host_info_frame, text="OS:")
        self.lblHostOS.grid(row=0, column=2)

        self.lblHostOSValue = tkinter.Label(self.host_info_frame, text=self.host.get_system())
        self.lblHostOSValue.grid(row=0, column=3, columnspan=3)

        self.lblInterfaces = tkinter.Label(self.host_info_frame, text="Available Interfaces:")
        self.lblInterfaces.grid(row=1, column=0)

        self.interfaces_formated = []
        for eth in self.host.get_interfaces():
            self.interfaces_formated.append(f"{eth['network']}/{eth['cider']}")

        self.combo_interfaces = ttk.Combobox(self.host_info_frame, values=self.interfaces_formated, state="readonly")
        self.combo_interfaces.grid(row=1, column=1)

        self.btn_sweep_net = tkinter.Button(self.host_info_frame, text="Sweep Network", command=self.sweep_action)
        self.btn_sweep_net.grid(row=1, column=3, columnspan=3)

        for widget in self.host_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # self.show_progress_bar()



    def show_progress_bar(self, thread):
        self.progress_frame = tkinter.LabelFrame(self.root, relief="flat")
        # self.host_info_frame.pack(side = "left", fill = tkinter.BOTH, expand = 1)
        self.progress_frame.grid(row=1, column=0, padx=8, pady=0, sticky="news")
        progressBar = ttk.Progressbar(self.progress_frame, mode='indeterminate', length=453)
        progressBar.grid(row=0, column=0, padx=10, pady=5)
        progressBar.start(interval=35)
        while thread.is_alive():
            root.update()


    def show_active_hosts(self):
        # Sweep results
        results_frame = tkinter.LabelFrame(self.root, text="Active Hosts")
        # self.results_frame.pack(side = "left", fill = tkinter.BOTH, expand = 1)
        results_frame.grid(row=1, column=0, sticky="news", padx=20, pady=5)

        lbl_active_host = tkinter.Label(results_frame, text="Active Hosts")
        lbl_active_host.grid(row=0, column=0)

        self.listBox = tkinter.Listbox(results_frame)
        self.listBox.grid(row=0, column=0 , )

        self.btn_sweep_port = tkinter.Button(results_frame, text="Find Open Ports", command=self.find_ports_action)
        self.btn_sweep_port.grid(row=0, column=2)

        self.txtArea = tkinter.Text (results_frame, bg="#d3dce6", state="disabled", width=20, height=10)
        self.txtArea.grid(row=0, column=3)

        for i in range(len(self.active_hosts)):
            self.listBox.insert(i, self.active_hosts[i])

        for widget in results_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

    def hide(self):
        if self.hidden == 0:
            self.results_frame.destroy()



# window.title("NetScanner - Prototype")
# window.iconphoto(False, tkinter.PhotoImage(file="img/title_icon.png"))
# window.geometry("720x550")
# window.resizable(False, False)
# frame = tkinter.Frame(window)
# frame.pack()

root = tkinter.Tk()
app = App(root)
root.mainloop()
