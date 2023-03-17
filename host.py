class Host(object):

    def __init__(self, ip, port):
        self.ip_addr = ip
        self.port = port

    def getIp(self):
        return self.ip_addr

    def getPort(self):
        return self.port
