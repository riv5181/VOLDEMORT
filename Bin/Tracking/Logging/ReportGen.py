from time import gmtime, strftime

def createReport(currSettings,db, cur, numPackets, numAfter, numFlows, withFlood):
    location = "/home/voldemort/Desktop/IMPLEMENTATION/Bin/Tracking/Logging/logs/"
    fileName = str(strftime("%m-%d-%Y %H:%M:%S", gmtime()))

    report = open(location+fileName+".log","w")

    report.write("FLOODED: ") #Insert Protocol and/or Services. Will use separate function.
    report.write("")
    report.write("===== CYCLE INFORMATION ======")
    report.write("Date Started: ")
    report.write("Time Started: ")
    report.write("Date Ended: ")
    report.write("Time Ended: ")
    report.write(" ")
    report.write("===== STATISTICS =====")
    report.write("Nummber of packets obtained: " + numPackets)
    report.write("Number of packets after filtering: " + numAfter)
    report.write("Flows detected: " + numFlows)
    report.write("Flows with flooding: " + withFlood)
    report.write(" ")
    report.write("===== THRESHOLD VALUES =====") #Service (Percentage) Threshold WILL ALWAYS stay the same, but it
    report.write("Old TCP value: ")              #doesn't mean it won't be logged. It adjusts based on prot threshold.
    report.write("Old UDP value: ")
    report.write("Old ICMP value: ")
    report.write("New TCP value: ")
    report.write("New UDP value: ")
    report.write("New ICMP value: ")
    report.write(" ")
    report.write("===== SUSPICION COUNT =====") #Insert ONLY the IP addresses involved in THIS cycle
    report.write("IP Address: ") #Will be looped and/or might use a separate function
    report.write("Count: ")
    report.write(" ")

    report.close()