import ipaddress
import tkinter
from tkinter import ttk
from tkinter import messagebox
from localhost import Localhost
from discovery import Discovery

active_hosts = []
def sweep_action():

    selected_network = combo_interfaces.get()
    if selected_network == '':
        messagebox.showerror("::Error Message::", "Please, choose one network to scan!")
    else:
        varredura = Discovery()
        net = ipaddress.IPv4Network(selected_network)  # nao apagar
        my_ip = host.get_ip_by_network(selected_network)
        varredura.network_scan(my_ip, net)  # nao apagar
        # varredura.port_scan('192.168.0.110')
        active_hosts = sorted(varredura.get_active_hosts(), key=ipaddress.IPv4Address)  # nao apagar
        for item in active_hosts:
            listBox.insert(tkinter.END, item)

        if len(active_hosts) > 0:
            results_frame

host = Localhost()

window = tkinter.Tk()
window.title("NetScanner - Prototype")
window.iconphoto(False, tkinter.PhotoImage(file="img/title_icon.png"))
# window.geometry("720x550")
window.resizable(False, False)

frame = tkinter.Frame(window)
frame.pack()

host_info_frame = tkinter.LabelFrame(frame, text="Host Information")
host_info_frame.grid(row=0, column=0, padx=20, pady=5)

lblHostname = tkinter.Label(host_info_frame, text="Name:")
lblHostname.grid(row=0, column=0)

lblHostnameValue = tkinter.Label(host_info_frame, text=host.get_hostname())
lblHostnameValue.grid(row=0, column=1)

lblHostOS = tkinter.Label(host_info_frame, text="OS:")
lblHostOS.grid(row=0, column=2)

lblHostOSValue = tkinter.Label(host_info_frame, text=host.get_system())
lblHostOSValue.grid(row=0, column=3)

lblInterfaces = tkinter.Label(host_info_frame, text="Available Interfaces:")
lblInterfaces.grid(row=1, column=0)

interfaces_formated = []
for eth in host.get_interfaces():
    interfaces_formated.append(f"{eth['network']}/{eth['cider']}")


combo_interfaces = ttk.Combobox(host_info_frame, values=interfaces_formated, state="readonly")
combo_interfaces.grid(row=1, column=1)

button = tkinter.Button(host_info_frame, text="Sweep Network", command=sweep_action)
button.grid(row=1, column=3, columnspan=3)

for widget in host_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Sweep results

results_frame = tkinter.LabelFrame(frame, text="Active Hosts")
results_frame.grid(row=1, column=0, sticky="news", padx=20, pady=5)

# lblActiveHost = tkinter.Label(results_frame, text="Active Hosts")
# lblActiveHost.grid(row=0, column=0)

listBox = tkinter.Listbox(results_frame)
listBox.grid(row=0, column=0)

for item in active_hosts:
    listBox.insert(tkinter.END, item)

for widget in results_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

results_frame.destroy()
window.mainloop()


# print(host)
# lst_ifaces = host.get_interfaces()

# for i in range(len(lst_ifaces)):
#     network = ipaddress.IPv4Network(f"{lst_ifaces[i]['network']}/{lst_ifaces[i]['cider']}")
#     sweep = Discovery()
#     sweep.network_scan(lst_ifaces[i]['ip_addr'], network)
#     print(sweep.get_active_hosts())
#     print(list[i]['ip_addr'])
#     print(list[i]['network'])