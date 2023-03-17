import socket
import threading


class Host(object):

    def __init__(self, ip):
        self.ip_addr = ip
        self.opened_ports = []

    def __call__(self, *args, **kwargs):
        self.port_scan()

    def getIp(self):
        return self.ip_addr

    def getOpenedPort(self):
        return self.opened_ports

    @staticmethod
    def check_open_port(ipaddr, port, services, lock):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ipaddr, port))
        if result == 0:
            with lock:
                services.append(port)
        s.close()

    def port_scan(self):
        threads = []
        lock = threading.Lock()
        lista = [135,139,445,1236,3389]
        for port in lista:
            t = threading.Thread(target=self.check_open_port, args=(self.getIp(), port, self.opened_ports, lock,))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

if __name__ == '__main__':
    host = Host('10.3.18.62')
    host.port_scan()
    print(host.getOpenedPort())