import scapy.all as scapy

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    # scapy.ls(scapy.Arp())
    # print(arp_request.summary())
    arp_request.show()
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    # scapy.ls(scapy.Ether())
    # print(broadcast.summary())
    broadcast.show()
    arp_request_broadcast = broadcast/arp_request
    # print(arp_request_broadcast.summary)
    arp_request_broadcast.show()

# scan('192.168.254.1/24')
scan('192.168.254.1')
