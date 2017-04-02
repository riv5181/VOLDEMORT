import sys, socket, fcntl, struct, MySQLdb, Preprocessor, StatControl, FloodDetection, Tracking, Logging
from time import gmtime, strftime, localtime
from threading import Thread
from classes import packet as thePacket

packets = []
flows = []
data = []
currSettings = StatControl.adminSettings
device1 = currSettings.device
maxTime1 = currSettings.maxTime
network = currSettings.network
timeStart = ''
timeEnd = ''
floodEvent = False

#Connector to logging database
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="p@ssword",db="voldemortdb")
cur = db.cursor()

#Get PC's IP. Takes few seconds to obtain. Will delay startup of VOLDEMORT.
def getIPAddress(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

mainIP = str(getIPAddress(device1))

cur.execute("SELECT MAX(cycle_time) FROM cycle")
obtainedcurID = cur.fetchall()
Tracking.setCurrCycleTime(int(obtainedcurID[0][0]) + 1)

try:
    while True:
        timeStart = strftime("%m-%d-%Y %H:%M:%S", localtime())
        packets = Preprocessor.obtainPackets(device1, maxTime1)
        timeEnd = strftime("%m-%d-%Y %H:%M:%S", localtime())

        print('BEFORE FILTER: ' + str(len(packets)))
        blah1 = len(packets)
        packets = Preprocessor.filterObtainedPackets(packets, mainIP, network)
        print('AFTER FILTER: ' + str(len(packets)))
        blah2 = len(packets)
        noFPackets = packets
        print(' ')

        ifFlood = Preprocessor.analyzePacketswThresh(packets,currSettings)
        floodEvent = Preprocessor.getFloodingEvent()

        if ifFlood or floodEvent:
            Tracking.setFloodingNoExist(False)
            flows = FloodDetection.fDModule(packets, currSettings)
            blah3 = FloodDetection.getFlowBefore()
            blah4 = FloodDetection.getNumFloods()
            data = Tracking.tracker(flows, currSettings, timeStart, timeEnd, db, cur)

            if data == None:
                timeStart = ''
                timeEnd = ''
                packets = []
                flows = []
                Logging.createReport(currSettings,Tracking.getCurrCycleTime(), cur, blah1, blah2, blah3, blah4,
                                     FloodDetection.getLenPackets())

            else:
                print('-----OLD THRESHOLDS-----')
                print('TCP: ' + str(currSettings.tcpThreshold))
                print(' ')
                print('UDP: ' + str(currSettings.udpThreshold))
                print(' ')
                print('ICMP: ' + str(currSettings.icmpThreshold))
                print(' ')

                currSettings = StatControl.updateThreshold(data,currSettings, StatControl.adminSettings, db, cur)
                Logging.createReport(currSettings, Tracking.getCurrCycleTime(), cur, blah1, blah2, blah3, blah4,
                                     FloodDetection.getLenPackets())
                Tracking.setCurrCycleTime(Tracking.getCurrCycleTime() + 1)

                print('-----NEW THRESHOLDS-----')
                print('TCP: ' + str(currSettings.tcpThreshold))
                print(' ')
                print('UDP: ' + str(currSettings.udpThreshold))
                print(' ')
                print('ICMP: ' + str(currSettings.icmpThreshold))
                print(' ')

                if Tracking.getFloodingNoExist():
                    Preprocessor.setFloodingEvent(False)

                #raw_input("Press Enter to Continue")

        else:
            Logging.createReportNoFlood(currSettings, timeStart, timeEnd, blah2, noFPackets)
            packets = []
            flows = []
            timeStart = ''
            timeEnd = ''
            recorded = []
            noFPackets = []

except KeyboardInterrupt:
    print('QUIT!')

db.close()
