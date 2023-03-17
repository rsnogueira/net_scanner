import os
import socket
import threading
import ipaddress
from host import Host


class Discovery(object):

    def __init__(self):
        self.active_hosts = []

    def get_active_hosts(self):
        return self.active_hosts

    @staticmethod
    def check_active_ping(ip_addr, active_hosts, lock):
        ports = []
        result = os.popen("ping {0} -n 1".format(ip_addr)).read()

        if "TTL" in result:
            with lock:
                # ports = Host.port_scan(ip_addr)
                # active_hosts.append(Host(str(ip_addr),ports))
                active_hosts.append(str(ip_addr))


    def network_scan(self, my_ip, network):
        threads = []
        lock = threading.Lock()
        cont = 0
        for addr in network:
            if my_ip == str(addr):
                continue

            t = threading.Thread(target=self.check_active_ping, args=(addr, self.active_hosts, lock,))
            t.start()
            threads.append(t)

            cont += 1
            if cont > 10:
                 break
        for thread in threads:
            thread.join()

    @staticmethod
    def port_scan(target):
        services = []
        port = 4444
        # for port in range(1, 25):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect((target, port))
        if result == 0:
            services.append(port)
        # s.close()

        return services



if __name__ == '__main__':
    varredura = Discovery()
    # net = ipaddress.IPv4Network('192.168.0.0/24')
    rede = ipaddress.IPv4Network('10.0.0.0/29')
    # varredura.network_scan('192.168.0.106', net)
    varredura.port_scan('192.168.0.110')
    print(varredura.get_active_hosts())
