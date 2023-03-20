import socket
import threading
from datetime import datetime


class Host(object):

    def __init__(self, ip):
        self.ip_addr = ip
        self.opened_ports = []
        self.dict_services = {7: 'Echo',
                              20: 'FTP-data',
                              21: 'FTP',
                              22: 'SSH-SCP',
                              23: 'Telnet',
                              25: 'SMTP',
                              53: 'DNS',
                              69: 'TFTP',
                              80: 'HTTP',
                              88: 'Kerberos',
                              102: 'Iso-tsap',
                              110: 'POP3',
                              135: 'Microsoft EPMAP',
                              137: 'NetBIOS-ns',
                              139: 'NetBIOS-ssn',
                              143: 'IMAP4',
                              443: 'HTTP',
                              464: 'Kerberos',
                              465: 'SMTP',
                              587: 'SMTP',
                              593: 'Microsoft DCOM',
                              636: 'LDAPS',
                              691: 'MS Exchange',
                              902: 'VMware Server',
                              989: 'FTP over SSL',
                              990: 'FTP over SSL',
                              993: 'IMAP4 over SSL',
                              995: 'POP3 over SSL',
                              1025: 'Microsoft RPC',
                              3389: 'RPD'
                              }


    def __call__(self, *args, **kwargs):
        self.port_scan()

    def getIp(self):
        return self.ip_addr

    def getAvailableServices(self):
        formated_ports = ""
        svc_name = ""
        for i in range(len(self.opened_ports)):
            svc_name = self.dict_services.get(self.opened_ports[i], 'Unknown Svc')
            formated_ports += ('{0} - {1}\n'.format(svc_name, self.opened_ports[i]))

        return formated_ports


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
        t1 = datetime.now()
        lista = [22,135,139,445,1236,3389,4444]
        # for port in lista:
        for port in range(1,1025):
            t = threading.Thread(target=self.check_open_port, args=(self.getIp(), port, self.opened_ports, lock,))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        t2 = datetime.now()
        print(f"Scanning {len(lista)} ports in: {t2 - t1}")

if __name__ == '__main__':
    host = Host('10.3.18.62')
    host.port_scan()
    print(host.getAvailableServices())