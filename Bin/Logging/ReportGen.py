from time import gmtime, strftime

def printResult(cur, query):
    string = ""
    cur.execute(query)
    output = cur.fetchall()

    i = 0
    j = 0
    while i < len(output):
        while j < len(output[i]):
            string = string + str(output[i][j])
            string = string + " "
            j = j + 1
        i = i + 1

    return string

def createReport(currSettings,db, cur, numPackets, numAfter, numFlows, withFlood):
    location = "/home/voldemort/Desktop/IMPLEMENTATION/Bin/Tracking/Logging/logs/"
    fileName = str(strftime("%m-%d-%Y %H:%M:%S", gmtime()))

    report = open(location+fileName+".log","w")
    query = "SELECT protocol, service FROM flow f WHERE idcycle = (SELECT max(idcycle) FROM cycle) AND status = 1"
    report.write("FLOODED: " + printResult(cur,query)) #Insert Protocol and/or Services. Will use separate function.
    report.write("")

    report.write("===== CYCLE INFORMATION ======")
    query = "SELECT date_start FROM cycle WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Date Started: " + printResult(cur,query))
    query = "SELECT time_start FROM  cycle WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Time Started: " + printResult(cur,query))
    query = "SELECT date_end FROM cycle WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Date Ended: " + printResult(cur,query))
    query = "SELECT time_end  FROM cycle WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Time Ended: " + printResult(cur,query))
    report.write(" ")

    report.write("===== STATISTICS =====")
    report.write("Nummber of packets obtained: " + str(numPackets))
    report.write("Number of packets after filtering: " + str(numAfter))
    report.write("Flows detected: " + str(numFlows))
    report.write("Flows with flooding: " + str(withFlood))
    report.write(" ")

    # Service (Percentage) Threshold WILL ALWAYS stay the same, but it
    # doesn't mean it won't be logged. It adjusts based on prot threshold, technically.
    report.write("===== THRESHOLD VALUES =====")
    query = "SELECT old_tcp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Old TCP value: " + printResult(cur,query))
    query = "SELECT old_udp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Old UDP value: " + printResult(cur,query))
    query = "SELECT old_icmp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("Old ICMP value: " + printResult(cur,query))
    query = "SELECT new_tcp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("New TCP value: " + printResult(cur,query))
    query = "SELECT new_udp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("New UDP value: " + printResult(cur,query))
    query = "SELECT new_icmp FROM threshold WHERE idcycle = (SELECT max(idcycle) FROM cycle)"
    report.write("New ICMP value: " + printResult(cur,query))
    report.write(" ")

    # Insert ONLY the IP addresses involved in THIS cycle
    report.write("===== SUSPICION COUNT =====")
    cur.execute("SELECT src_ip 'IP Address', count(src_ip) 'suspicion count' FROM flow " \
                "WHERE idcycle = (SELECT max(idcycle) FROM cycle) GROUP BY src_ip")
    output = cur.fetchall()
    i = 0
    j = 0
    while i < len(output):
        report.write("IP Address: " + str(output[i][j]))
        j = j + 1
        report.write("Count: ")
        report.write(" ")
        i = i + 1
        j = 0

    report.close()