import os
import socket
import threading
import ipaddress


class Discovery(object):

    def __init__(self):
        self.active_hosts = []

    def get_active_hosts(self):
        return self.active_hosts

    @staticmethod
    def check_active_ping(ip_addr, active_hosts, lock):
        host = {}
        result = os.popen("ping {0} -n 1".format(ip_addr)).read()

        if "TTL" in result:
            with lock:
                host['ip_addr'] = str(ip_addr)
                active_hosts.append(host)

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
            if cont > 3:
                break
        for thread in threads:
            thread.join()

    def port_scan(self, target):
        host_ativo = {}
        services = {}
        lsf_services = []
        for port in range(1, 1025):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect((target, port))
            if result == 0:
                services['port'] = str(port)
                services['status'] = 'OPEN'
                lsf_services.append(services)
        s.close()

        # for i in range(len(self.active_hosts)):
        #     host_ativo = self.active_hosts[i]
        #     if host_ativo['ip_addr'] == target:
        #         host_ativo.



if __name__ == '__main__':
    varredura = Discovery()
    net = ipaddress.IPv4Network('10.3.18.0/24')
    # rede = ipaddress.IPv4Network('10.0.0.0/29')
    varredura.network_scan('10.3.18.4', net)
    print(varredura.get_active_hosts())
