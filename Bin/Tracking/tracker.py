#import Logging

cycle_count = 0
cycle_noFlood = 0
noMoreFlood = False
tcpsyn = []
tcpsynack = []
tcphttp = []
udpdns = []
udpdhcp = []
icmp = []
tcp = []
udp = []

def getFloodingNoExist():
    return noMoreFlood

def setFloodingNoExist(event):
    global noMoreFlood
    noMoreFlood = event

def checkDataSize(flows, service):
    totalData = 0
    max = len(flows)
    i = 0

    while i < max:
        if flows[i].protocol == 'TCP' and flows[i].isFlood == True:
            if flows[i].pktFlag == service or flows[i].service == service:
                totalData = totalData + int(flows[i].datasize)
                i = i + 1

            else:
                i = i + 1

        elif (flows[i].protocol == 'UDP' or flows[i].protocol == 'ICMP') and flows[i].isFlood == True:
            if flows[i].service == service:
                totalData = totalData + int(flows[i].datasize)
                i = i + 1

            else:
                i = i + 1

        else:
            i = i + 1

    return totalData

def checkDataSizeSimplified(flows, protocol):
    totalData = 0
    max = len(flows)
    i = 0

    while i < max:
        if flows[i].protocol == protocol and flows[i].isFlood == True:
            totalData = totalData + int(flows[i].datasize)

        i = i + 1

    return totalData

def checkFloodingExist(flows):
    i = 0
    max = len(flows)

    while i < max:
        if flows[i].isFlood == True:
            return True

        i = i + 1

    return False

def calculateThreshold(totalThresh, threshPercentage):
    return 0.01 * (int(totalThresh) * int(threshPercentage))

def tracker(flows, settings, timeStart, timeEnd, db, cur):
    global cycle_count, cycle_noFlood, tcpsyn, tcpsynack, tcphttp, udpdns, udpdhcp, icmp, tcp, udp, noMoreFlood
    data = []

    if checkFloodingExist(flows):
        #Insert code to put flows to logging module
        noMoreFlood = False
        '''
        cur.execute("INSERT INTO cycle (date_start,time_start,date_end,time_end) VALUES (%s, %s, %s, %s)",
                    (timeStart[0:10],timeStart[11:19],timeEnd[0:10],timeEnd[11:19]))
        db.commit()
        cur.execute("SELECT MAX(idcycle) FROM cycle")
        obtainedcurID = cur.fetchall()
        curID = int(obtainedcurID[0][0])
        i = 0
        max = len(flows)
        while i < max:
            if flows[i].isFlood == True:
                cur.execute("INSERT INTO flow (idcycle,src_ip,dest_ip,protocol,service,packetflg,datasize) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)",(curID,flows[i].sourceIP,flows[i].destIP,
                            flows[i].protocol,flows[i].service,flows[i].pktFlag,flows[i].datasize))
                db.commit()

            i = i + 1
        #'''

    tcpThresh = calculateThreshold(settings.bandwidth, settings.tcpThreshold)
    udpThresh = calculateThreshold(settings.bandwidth, settings.udpThreshold)

    tcpsyn.append((float(checkDataSize(flows, 'SYN')) / tcpThresh) * 100)
    tcpsynack.append((float(checkDataSize(flows, 'SYN-ACK')) / tcpThresh) * 100)
    tcphttp.append((float(checkDataSize(flows, 'HTTP')) / tcpThresh) * 100)
    udpdns.append((float(checkDataSize(flows, 'DNS')) / udpThresh) * 100)
    udpdhcp.append((float(checkDataSize(flows, 'DHCP'))/ udpThresh) * 100)
    icmp.append((float(checkDataSizeSimplified(flows, 'ICMP')) / settings.bandwidth) * 100)
    tcp.append((float(checkDataSizeSimplified(flows, 'TCP')) / settings.bandwidth) * 100)
    udp.append((float(checkDataSizeSimplified(flows, 'UDP')) / settings.bandwidth) * 100)
    cycle_count = cycle_count + 1

    if checkFloodingExist(flows): cycle_noFlood = 0
    else: cycle_noFlood = cycle_noFlood + 1

    if cycle_noFlood >= settings.cycle_time: noMoreFlood = True

    if cycle_count >= settings.cycle_time or cycle_noFlood >= settings.cycle_time:
        cycle_count = 0
        cycle_noFlood = 0
        data.append(tcpsyn)  # data[0]
        data.append(tcpsynack)  # data[1]
        data.append(tcphttp)  # data[2]
        data.append(udpdns)  # data[3]
        data.append(udpdhcp)  # data[4]
        data.append(icmp)  # data[5]
        data.append(tcp) # data[6]
        data.append(udp) # data[7]git

        tcpsyn = []
        tcpsynack = []
        tcphttp = []
        udpdns = []
        udpdhcp = []
        icmp = []
        tcp = []
        udp = []

        return data

    return None
