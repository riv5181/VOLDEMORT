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
    max = len(oPackets)

    #this segment already removes unnecessary ICMP
    while i < max:
        if oPackets[i].sourceIP == getIPAddress(device):
            oPackets.remove(oPackets[i])

        #only involved if TCP packet is either HTTP, or if it uses the SYN or SYN-ACK flag. Assigned at packetReceiver
        elif oPackets[i].protocol == 'TCP' and oPackets[i].service == 'OTHER' and oPackets[i].flag == 'OTHER':
            oPackets.remove(oPackets[i])

        #only involved if UDP packet is either DNS or DHCP service. Assigned at packetReceiver
        elif oPackets[i].protocol == 'UDP' and oPackets[i].service == 'OTHER':
            oPackets.remove(oPackets[i])

        max = len(oPackets)
        i = i + 1

    return oPackets