from time import gmtime, strftime

def createReport(currSettings,db, cur, dist):
    location = "/home/voldemort/Desktop/IMPLEMENTATION/Bin/Logging/logs/"
    fileName = str(strftime("%m-%d-%Y %H:%M:%S", gmtime()))

    report = open(location+fileName+".log","w")

    report.write("Seig Heil!")

    report.close()