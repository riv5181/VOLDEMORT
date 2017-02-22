#import Logging

cycle_count = 0
cycle_noFlood = 0
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

def checkFloodingExist(flows):
    i = 0
    max = len(flows)

    while i < max:
        if flows[i].isFlood == True:
            return True

        i = i + 1

    return False

def tracker(flows, settings, timeStart, timeEnd, db, cur):
    global cycle_count, cycle_noFlood, tcpsyn, tcpsynack, tcphttp, udpdns, udpdhcp, icmp
    data = []

    if checkFloodingExist(flows):
        #Insert code to put flows to logging module
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

    tcpsyn.append((checkDataSize(flows, 'SYN') / settings.bandwidth) * 100)
    tcpsynack.append((checkDataSize(flows, 'SYN-ACK') / settings.bandwidth) * 100)
    tcphttp.append((checkDataSize(flows, 'HTTP') / settings.bandwidth) * 100)
    udpdns.append((checkDataSize(flows, 'DNS') / settings.bandwidth) * 100)
    udpdhcp.append((checkDataSize(flows, 'DHCP') / settings.bandwidth) * 100)
    icmp.append((checkDataSize(flows, 'ECHO-REPLY') / settings.bandwidth) * 100)
    cycle_count = cycle_count + 1

    if checkFloodingExist(flows): cycle_noFlood = 0
    else: cycle_noFlood = cycle_noFlood + 1

    if cycle_count >= settings.cycle_time or cycle_count >= settings.cycle_time:
        cycle_count = 0
        data.append(tcpsyn)  # data[0]
        data.append(tcpsynack)  # data[1]
        data.append(tcphttp)  # data[2]
        data.append(udpdns)  # data[3]
        data.append(udpdhcp)  # data[4]
        data.append(icmp)  # data[5]

        tcpsyn = []
        tcpsynack = []
        tcphttp = []
        udpdns = []
        udpdhcp = []
        icmp = []

        return data

    return 'NULL'
