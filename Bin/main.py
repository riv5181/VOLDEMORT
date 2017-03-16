import sys, socket, fcntl, struct, MySQLdb, Preprocessor, StatControl, FloodDetection, Tracking, Logging
from time import gmtime, strftime
from threading import Thread
from classes import packet as thePacket

packets = []
flows = []
data = []
currSettings = StatControl.adminSettings
adminSettings = StatControl.adminSettings
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

try:
    while True:
        timeStart = strftime("%m-%d-%Y %H:%M:%S", gmtime())
        packets = Preprocessor.obtainPackets(device1, maxTime1)
        timeEnd = strftime("%m-%d-%Y %H:%M:%S", gmtime())

        print('BEFORE FILTER: ' + str(len(packets)))
        packets = Preprocessor.filterObtainedPackets(packets, mainIP, network)
        print('AFTER FILTER: ' + str(len(packets)))
        print(' ')

        ifFlood = Preprocessor.analyzePacketswThresh(packets,currSettings)
        floodEvent = Preprocessor.getFloodingEvent()

        if ifFlood or floodEvent:
            Tracking.setFloodingNoExist(False)
            flows = FloodDetection.fDModule(packets, currSettings)

            if len(flows) > currSettings.maxFlows:
                Preprocessor.setFloodingEvent(False)
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
                Logging.createReport(currSettings,db,cur,"dist")
                #'''

            else:
                data = Tracking.tracker(flows, currSettings, timeStart, timeEnd, db, cur)

                if data == None:
                    timeStart = ''
                    timeEnd = ''
                    packets = []
                    flows = []

                else:
                    print('-----OLD THRESHOLDS-----')
                    print('TCP: ' + str(currSettings.tcpThreshold))
                    print('TCP SYN: ' + str(currSettings.synThresh))
                    print('TCP SYN-ACK: ' + str(currSettings.synackThresh))
                    print('TCP HTTP: ' + str(currSettings.httpThresh))
                    print(' ')
                    print('UDP: ' + str(currSettings.udpThreshold))
                    print('UDP DNS: ' + str(currSettings.dnsThresh))
                    print('UDP DHCP: ' + str(currSettings.dhcpThresh))
                    print(' ')
                    print('ICMP: ' + str(currSettings.icmpThreshold))
                    print(' ')

                    currSettings = StatControl.updateThreshold(data,adminSettings)

                    print('-----NEW THRESHOLDS-----')
                    print('TCP: ' + str(currSettings.tcpThreshold))
                    print('TCP SYN: ' + str(currSettings.synThresh))
                    print('TCP SYN-ACK: ' + str(currSettings.synackThresh))
                    print('TCP HTTP: ' + str(currSettings.httpThresh))
                    print(' ')
                    print('UDP: ' + str(currSettings.udpThreshold))
                    print('UDP DNS: ' + str(currSettings.dnsThresh))
                    print('UDP DHCP: ' + str(currSettings.dhcpThresh))
                    print(' ')
                    print('ICMP: ' + str(currSettings.icmpThreshold))
                    print(' ')

                    if Tracking.getFloodingNoExist():
                        Preprocessor.setFloodingEvent(False)

                    raw_input("Press Enter to continue...")

        else:
            packets = []
            flows = []
            timeStart = ''
            timeEnd = ''

except KeyboardInterrupt:
    print('QUIT!')

db.close()
print (timeStart + " " + timeEnd)
