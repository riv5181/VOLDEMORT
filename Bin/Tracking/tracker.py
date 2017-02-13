#import Logging

cycle_count = 0
tcpsyn = []
tcpsynack = []
tcphttp = []
udpdns = []
udpdhcp = []
icmp = []

def checkDataSize(flows, service):
    totalData = 0
    max = len(flows)
    i = 0

    while i < max:
        if flows[i].protocol == 'TCP':
            if flows[i].pktFlag == service or flows[i].service == service:
                totalData = totalData + int(flows[i].datasize)
                i = i + 1

            else:
                i = i + 1

        elif flows[i].protocol == 'UDP' or flows[i].protocol == 'ICMP':
            if flows[i].service == service:
                totalData = totalData + int(flows[i].datasize)
                i = i + 1

            else:
                i = i + 1

        else:
            i = i + 1

    return totalData

def tracker(flows, settings):
    global cycle_count, tcpsyn, tcpsynack, tcphttp, udpdns, udpdhcp, icmp
    data = []

    #Insert code to put flows to logging module


    tcpsyn.append((checkDataSize(flows,'SYN') / settings.bandwidth) * 100)
    tcpsynack.append((checkDataSize(flows, 'SYN-ACK') / settings.bandwidth) * 100)
    tcphttp.append((checkDataSize(flows, 'HTTP') / settings.bandwidth) * 100)
    udpdns.append((checkDataSize(flows, 'DNS') / settings.bandwidth) * 100)
    udpdhcp.append((checkDataSize(flows, 'DHCP') / settings.bandwidth) * 100)
    icmp.append((checkDataSize(flows, 'ECHO-REPLY') / settings.bandwidth) * 100)
    cycle_count = cycle_count + 1

    if cycle_count >= settings.cycle_time:
        cycle_count = 0
        data.append(tcpsyn) #data[0]
        data.append(tcpsynack) #data[1]
        data.append(tcphttp) #data[2]
        data.append(udpdns) #data[3]
        data.append(udpdhcp) #data[4]
        data.append(icmp) #data[5]

        tcpsyn = []
        tcpsynack = []
        tcphttp = []
        udpdns = []
        udpdhcp = []
        icmp = []

        return data

    return 'NULL'
