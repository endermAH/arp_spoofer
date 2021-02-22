#!venv/bin/python

import scapy.all as scapy
from pprint import pprint


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)
    return answered_list


if __name__ == "__main__":
    mac = get_mac("192.168.56.102")
    print(pprint(mac))
