import ipaddress

from localhost import Localhost
from discovery import Discovery


host = Localhost()
lst_ifaces = host.get_interfaces()

for i in range(len(lst_ifaces)):
    network = ipaddress.IPv4Network(f"{lst_ifaces[i]['network']}/{lst_ifaces[i]['cider']}")
    sweep = Discovery()
    sweep.network_scan(lst_ifaces[i]['ip_addr'], network)
    print(sweep.get_active_hosts())
    # print(list[i]['ip_addr'])
    # print(list[i]['network'])