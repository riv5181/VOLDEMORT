import socket, fcntl, struct
from classes import packet as thePacket

#gets own IP Address
def getIPAddress(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def filterObtainedPackets(oPackets, device):
    i = 0

    while i < len(oPackets):
        if oPackets[i].sourceIP == getIPAddress(device):
            oPackets.remove(i)

        i = i + 1

        #remove other unnecessary TCP and UDP (only TCP HTTP GET, POST, SYN, SYN-ACK, UDP DNS, DHCP and ICMP ECHO-REPLY)

    return oPackets