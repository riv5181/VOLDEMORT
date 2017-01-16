
def segregatePackets(packets):
    sortedPackets = []
    tcpPackets = []
    udpPackets = []
    icmpPackets = []
    i = 0
    max = len(packets)

    while i < max:
        if packets[i].protocol == 'TCP':
            tcpPackets.append(packets[i])

        elif packets[i].protocol == 'UDP':
            udpPackets.append(packets[i])

        else:
            icmpPackets.append(packets[i])

        max = len(packets)
        i = i + 1

    sortedPackets.append(tcpPackets)
    sortedPackets.append(udpPackets)
    sortedPackets.append(icmpPackets)

    return sortedPackets