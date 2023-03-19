import os
import platform
import ipaddress


class Localhost(object):

    def __init__(self):
        self.system = platform.system()
        self.ip_addr = ""
        self.hostname = os.popen("hostname").read()[:-1]
        self.interfaces = []
        self.interfaces = self.set_interfaces()

    # def __init__(self, system, hostname, interfaces):
    #     self.system = system
    #     self.hostname = hostname
    #     self.interfaces = interfaces

    def get_system(self):
        return self.system

    def get_hostname(self):
        return self.hostname

    def get_interfaces(self):
        return self.interfaces

    def set_interfaces(self):
        host = {}
        cmd = "ipconfig"

        try:
            if self.system != "Windows":
                cmd = "ifconfig"

            for linha in os.popen(cmd).readlines():
                if "IPv4" in linha:
                    if linha[linha.find(":") + 2:-1] != '':
                        host['ip_addr'] = linha[linha.find(":") + 2:-1]
                if "Sub-rede" in linha or "Subnet" in linha:
                    # print(">>>" + linha[linha.find(":") + 2:-1] + "<<<")
                    if linha[linha.find(":") + 2:-1] != '':
                        host['netmask'] = linha[linha.find(":") + 2:-1]

                    host.update(self.get_network(host['ip_addr'], host['netmask']))
                    self.interfaces.append(host.copy())
        except:
            pass

        return self.interfaces

    def get_network(self, ip, netmask):
        network = {}
        ip_mask = ip + "/" + netmask
        try:
            net = ipaddress.IPv4Network(ipaddress.IPv4Interface(ip_mask).network)
            network['network'] = net.network_address
            network['cider'] = net.prefixlen
            network['broadcast'] = net.broadcast_address
            network['hosts'] = net.num_addresses
        except:
            pass

        return network

    def get_ip_by_network(self, network):

        for i in range(len(self.interfaces)):
            if network == f"{self.interfaces[i]['network']}/{self.interfaces[i]['cider']}":
                self.ip_addr = self.interfaces[i]['ip_addr']
                break

        return self.ip_addr

    def __str__(self):
        display = f"Hostname: {self.hostname}          OS: {self.system}\n"
        show_int = ""
        for i in range(len(self.interfaces)):
            show_int += (f"{20 * '***'}\n"
                        f"Interface[{i}]   \n"
                        f">>>>        IP: {self.interfaces[i]['ip_addr']}/{self.interfaces[i]['netmask']}\n"
                        f">>>>   Network: {self.interfaces[i]['network']}/{self.interfaces[i]['cider']}\n"
                        f">>>> Broadcast: {self.interfaces[i]['broadcast']}\n"
                        f">>>>     Hosts: {self.interfaces[i]['hosts']}\n")
        show_int += f"{30 * '**'}\n"

        display = display + show_int

        return display


if __name__ == '__main__':
    host = Localhost()
    print(host)
    # print(host.get_system())
    # print(host.get_hostname())
    print(host.get_interfaces())
    # host()
