import scapy.all as scapy

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    # answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1)
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # print(answered_list.summary())

    client_list = []
    for element in answered_list:
        client_dict = {'ip': element[1].psrc, 'mac': element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(result_list):
    print('IP\t\tAt MAC Address')
    print('-'*40)
    for client in result_list:
        print(client['ip'] + '\t\t' + client['mac'])

client_list = scan('192.168.254.1/24')
print_result(client_list)
