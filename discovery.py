import os
import socket
import threading
import ipaddress
from host import Host
from datetime import datetime

class Discovery(object):

    def __init__(self):
        self.active_hosts = []
        self.opened_ports = []

    def get_active_hosts(self):
        return self.active_hosts

    def get_opened_ports(self):
        return self.opened_ports

    @staticmethod
    def check_active_ping(ip_addr, active_hosts, lock):

        result = os.popen("ping {0} -n 1".format(ip_addr)).read()

        if "TTL" in result:
            with lock:
                # ports = Host.port_scan(ip_addr)
                # active_hosts.append(Host(str(ip_addr),ports))
                active_hosts.append(str(ip_addr))

    @staticmethod
    def check_open_port(ipaddr, port, services, lock):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ipaddr, port))
        if result == 0:
            with lock:
                services.append(port)
        s.close()

    def network_scan(self, my_ip, network):
        threads = []
        lock = threading.Lock()
        cont = 0
        t1 = datetime.now()
        for addr in network:
            # skip network / broadcast / current_ip
            if addr != network.network_address and addr != network.broadcast_address and my_ip != str(addr):
                t = threading.Thread(target=self.check_active_ping, args=(addr, self.active_hosts, lock,))
                t.start()
                threads.append(t)

                cont += 1
                # if cont > 10:
                #     break

        for thread in threads:
            thread.join()
        t2 = datetime.now()
        print(f"Scanning {cont} ws finished in: {t2 - t1}")



    def port_scan(self, target):
        threads = []
        lock = threading.Lock()
        lista = [135,139,445,1236,3389]
        for port in lista:
            t = threading.Thread(target=self.check_open_port, args=(target, port, self.opened_ports, lock,))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

if __name__ == '__main__':
    varredura = Discovery()
    net = ipaddress.IPv4Network('10.3.18.0/26') # nao apagar
    # rede = ipaddress.IPv4Network('10.0.0.0/29')
    varredura.network_scan('10.3.18.143', net) # nao apagar
    # varredura.port_scan('192.168.0.110')
    #print(sorted(varredura.get_active_hosts(), key=ipaddress.IPv4Address)) # nao apagar

    lista = sorted(varredura.get_active_hosts(), key=ipaddress.IPv4Address)

    for ip in lista:
        host = Host(ip)
        host.port_scan()
        print(f"IP: {ip}\n{host.getOpenedPort()}")

