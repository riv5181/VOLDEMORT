from time import gmtime, strftime

tcpData = 0
udpData = 0
icmpData = 0

def segregatePackets(packets):
    global tcpData, udpData, icmpData
    sortedPackets = []
    tcpPackets = []
    udpPackets = []
    icmpPackets = []
    i = 0
    max = len(packets)

    while i < max:
        if packets[i].protocol == 'TCP':
            tcpPackets.append(packets[i])
            tcpData = tcpData + packets[i].size

        elif packets[i].protocol == 'UDP':
            udpPackets.append(packets[i])
            udpData = udpData + packets[i].size

        else:
            icmpPackets.append(packets[i])
            icmpData = icmpData + packets[i].size

        max = len(packets)
        i = i + 1

    sortedPackets.append(tcpPackets)
    sortedPackets.append(udpPackets)
    sortedPackets.append(icmpPackets)

    return sortedPackets

def printResult(cur, query):
    string = ""
    cur.execute(query)
    output = cur.fetchall()

    i = 0
    j = 0
    while i < len(output):
        while j < len(output[i]):
            if string != 'NULL' or string != 'OTHER':
                string = string + str(output[i][j])
                string = string + " "
            j = j + 1
        i = i + 1

    return string

def createReport(curCycle, cur, numPackets, numAfter, numFlows, withFlood, lenPackets):
    location = "/home/voldemort/Desktop/IMPLEMENTATION/Bin/Logging/logs/"
    fileName = str(strftime("%m-%d-%Y %H:%M:%S", gmtime()))

    report = open(location+fileName+" C" +str(curCycle)+".log","w")
    query = "SELECT protocol, service, packetflg FROM flow f WHERE idcycle = (SELECT max(idcycle) FROM cycle) AND status = 1"
    report.write("FLOODED: " + printResult(cur,query) + "\n\n") #Insert Protocol and/or Services. Will use separate function.

    report.write("===== CYCLE INFORMATION ======" + "\n")
    query = "SELECT cycle_time FROM cycle WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Cycle Number: " + str(curCycle) + "\n")
    query = "SELECT date_start FROM cycle WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Date Started: " + printResult(cur,query) + "\n")
    query = "SELECT time_start FROM  cycle WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Time Started: " + printResult(cur,query) + "\n")
    query = "SELECT date_end FROM cycle WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Date Ended: " + printResult(cur,query) + "\n")
    query = "SELECT time_end  FROM cycle WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Time Ended: " + printResult(cur,query) + "\n\n")

    report.write("===== STATISTICS =====" + "\n")
    report.write("Nummber of packets obtained: " + str(numPackets) + "\n")
    report.write("Number of packets after filtering: " + str(numAfter) + "\n")
    report.write("Number of TCP packets after filtering: " + str(lenPackets[0]) + "\n")
    report.write("Number of UDP packets after filtering: " + str(lenPackets[1]) + "\n")
    report.write("Number of ICMP packets after filtering: " + str(lenPackets[2]) + "\n")
    report.write("Flows detected: " + str(numFlows) + "\n")
    report.write("Flows with flooding: " + str(withFlood) + "\n\n")

    # Service (Percentage) Threshold WILL ALWAYS stay the same, but it
    # doesn't mean it won't be logged. It adjusts based on prot threshold, technically.
    report.write("===== THRESHOLD VALUES =====" + "\n")
    query = "SELECT old_tcp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Old TCP value: " + printResult(cur,query) + "\n")
    query = "SELECT old_udp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Old UDP value: " + printResult(cur,query) + "\n")
    query = "SELECT old_icmp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Old ICMP value: " + printResult(cur,query) + "\n")
    query = "SELECT new_tcp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("New TCP value: " + printResult(cur,query) + "\n")
    query = "SELECT new_udp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("New UDP value: " + printResult(cur,query) + "\n")
    query = "SELECT new_icmp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("New ICMP value: " + printResult(cur,query) + "\n\n")

    # Insert ONLY the IP addresses involved in THIS cycle
    report.write("===== SUSPICION COUNT =====" + "\n")
    cur.execute("SELECT src_ip 'IP Address', count(src_ip) 'suspicion count' FROM flow " \
                "WHERE idcycle = (SELECT max(idcycle) FROM cycle) GROUP BY src_ip")
    output = cur.fetchall()
    i = 0
    j = 0
    while i < len(output):
        report.write("IP Address: " + str(output[i][j]) + "\n")
        j = j + 1
        report.write("Count: " + str(output[i][j]) + "\n\n")
        i = i + 1
        j = 0

    report.close()

def createReportNoFlood(currSettings, timeStart, timeEnd, numPackets, packets):
    global tcpData, udpData, icmpData
    tcpData = 0
    udpData = 0
    icmpData = 0

    location = "/home/voldemort/Desktop/IMPLEMENTATION/Bin/Logging/logs/"
    fileName = str(strftime("%m-%d-%Y %H:%M:%S NF", gmtime()))

    report = open(location+fileName+".log","w")

    report.write("===== CYCLE INFORMATION ======" + "\n")
    report.write("Time Started: " + timeStart + "\n")
    report.write("Time Ended: " + timeEnd + "\n\n")

    temp = segregatePackets(packets)

    report.write("===== STATISTICS =====" + "\n")
    report.write("Nummber of packets obtained (filtered): " + str(numPackets) + "\n")
    report.write("Number of TCP packets: " + str(len(temp[0])) + "\n")
    report.write("Size of ALL TCP packets: " + str(tcpData) + " bytes\n")
    report.write("Number of UDP packets: " + str(len(temp[1])) + "\n")
    report.write("Size of ALL UDP packets: " + str(udpData) + " bytes\n")
    report.write("Number of ICMP packets: " + str(len(temp[2])) + "\n")
    report.write("Size of ALL ICMP packets: " + str(icmpData) + " bytes\n\n")

    # Service (Percentage) Threshold WILL ALWAYS stay the same, but it
    # doesn't mean it won't be logged. It adjusts based on prot threshold, technically.
    report.write("===== THRESHOLD VALUES =====" + "\n")
    report.write("Old TCP value: " + str(currSettings.tcpThreshold) + "\n")
    report.write("Old UDP value: " + str(currSettings.udpThreshold) + "\n")
    report.write("Old ICMP value: " + str(currSettings.icmpThreshold) + "\n")
    report.write("New TCP value: " + str(currSettings.tcpThreshold) + "\n")
    report.write("New UDP value: " + str(currSettings.udpThreshold) + "\n")
    report.write("New ICMP value: " + str(currSettings.icmpThreshold) + "\n\n")

    report.close()
