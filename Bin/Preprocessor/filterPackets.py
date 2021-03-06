import socket, fcntl, struct
from netaddr import IPNetwork, IPAddress
from classes import packet as thePacket

#Filters obtained packets
def filterObtainedPackets(oPackets, mainIP, network):
    i = 0
    max = len(oPackets)
    newPackets = []

    #Checks the collected packets and removes unnecessary stuff
    while i < max:
        if oPackets[i].sourceIP != mainIP and IPAddress(oPackets[i].sourceIP) not in IPNetwork(network)\
                and (oPackets[i].sourceIP != "0.0.0.0" and oPackets[i].destIP != "255.255.255.255"):
            if oPackets[i].protocol == 'TCP':
                if oPackets[i].flag == 'SYN' or oPackets[i].flag == 'SYN-ACK':
                    newPackets.append(oPackets[i])
                    i = i + 1

                elif oPackets[i].service == 'HTTP':
                    newPackets.append(oPackets[i])
                    i = i + 1

                else:
                    i = i + 1

            elif oPackets[i].protocol == 'UDP':
                if oPackets[i].service == 'DNS' or oPackets[i].service == 'DHCP':
                    newPackets.append(oPackets[i])
                    i = i + 1

                else:
                    i = i + 1

            #ICMP only needs ECHO-REPLY, no more further checking needed
            elif oPackets[i].protocol == 'ICMP':
                newPackets.append(oPackets[i])
                i = i + 1

            else:
                i = i + 1

        else:
            i = i + 1

    #Returns a list of packets that is needed for analysis. Only contains protocols needed
    return newPackets