import socket, fcntl, struct
from classes import packet as thePacket

def filterObtainedPackets(oPackets, mainIP):
    i = 0
    max = len(oPackets)
    newPackets = []

    #this segment already removes unnecessary ICMP
    while i < max:
        if oPackets[i].sourceIP != mainIP:
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

            elif oPackets[i].protocol == 'ICMP':
                newPackets.append(oPackets[i])
                i = i + 1

            else:
                i = i + 1

        else:
            i = i + 1

        '''
        if oPackets[i].sourceIP == mainIP:
            oPackets.remove(oPackets[i])
            max = len(oPackets)
            i = i + 1

        #only involved if TCP packet is either HTTP, or if it uses the SYN or SYN-ACK flag. Assigned at packetReceiver
        elif oPackets[i].protocol == 'TCP' and (oPackets[i].service == 'OTHER' and oPackets[i].flag == 'OTHER'):
            oPackets.remove(oPackets[i])
            max = len(oPackets)
            i = i + 1

        #only involved if UDP packet is either DNS or DHCP service. Assigned at packetReceiver
        elif oPackets[i].protocol == 'UDP' and oPackets[i].service == 'OTHER':
            oPackets.remove(oPackets[i])
            max = len(oPackets)
            i = i + 1

        elif oPackets[i].service == 'OTHER' and (oPackets[i].flag == 'OTHER' or oPackets[i].flag == 'NULL'):
            oPackets.remove(oPackets[i])
            max = len(oPackets)
            i = i + 1

        else:
            max = len(oPackets)
            i = i + 1
        '''

    return newPackets