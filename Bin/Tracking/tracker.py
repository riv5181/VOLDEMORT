import Logging

cycle_count = 0
cycle_noFlood = 0
noMoreFlood = False
icmp = []
tcp = []
udp = []

def getFloodingNoExist():
    return noMoreFlood

def setFloodingNoExist(event):
    global noMoreFlood
    noMoreFlood = event

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

def tracker(flows, settings, timeStart, timeEnd, db, cur, recorded):
    global cycle_count, cycle_noFlood, icmp, tcp, udp, noMoreFlood#,tcpsyn, tcpsynack, tcphttp, udpdns, udpdhcp
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
                            "VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",(curID,flows[i].sourceIP,flows[i].destIP,
                            flows[i].protocol,flows[i].service,flows[i].pktFlag,flows[i].datasize, 1))
                db.commit()

            i = i + 1
        Logging.createReport(settings,db,cur,recorded[0],recorded[1],recorded[2],recorded[3])
        #'''

    if len(flows) > settings.maxFlows:
        # Insert code to put flows to logging module
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
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(curID,flows[i].sourceIP,flows[i].destIP,
                            flows[i].protocol,flows[i].service,flows[i].pktFlag,flows[i].datasize, 0))
                db.commit()

            i = i + 1
        Logging.createReport(settings,db,cur,recorded[0],recorded[1],recorded[2],recorded[3])
        #'''

    tcp.append((float(checkDataSizeSimplified(flows, 'TCP')) / settings.bandwidth) * 100)
    udp.append((float(checkDataSizeSimplified(flows, 'UDP')) / settings.bandwidth) * 100)
    icmp.append((float(checkDataSizeSimplified(flows, 'ICMP')) / settings.bandwidth) * 100)
    cycle_count = cycle_count + 1

    if checkFloodingExist(flows):
        cycle_noFlood = 0
    else:
        cycle_noFlood = cycle_noFlood + 1

    if cycle_noFlood >= settings.cycle_time:
        noMoreFlood = True

    if cycle_count >= settings.cycle_time or cycle_noFlood >= settings.cycle_time:
        cycle_count = 0
        cycle_noFlood = 0
        data.append(tcp) # data[0]
        data.append(udp) # data[1]
        data.append(icmp)  # data[2]

        tcp = []
        udp = []
        icmp = []

        return data

    return None
