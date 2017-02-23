import sys, socket, fcntl, struct, MySQLdb, Preprocessor, StatControl, FloodDetection, Tracking
from time import gmtime, strftime
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

try:
    while True:
        timeStart = strftime("%m-%d-%Y %H:%M:%S", gmtime())
        packets = Preprocessor.obtainPackets(device1, maxTime1)
        timeEnd = strftime("%m-%d-%Y %H:%M:%S", gmtime())

        print('BEFORE FILTER: ' + str(len(packets)))
        packets = Preprocessor.filterObtainedPackets(packets, mainIP, network)
        print('AFTER FILTER: ' + str(len(packets)))

        ifFlood = Preprocessor.analyzePacketswThresh(packets,currSettings)
        floodEvent = Preprocessor.getFloodingEvent()

        if ifFlood or floodEvent:
            Tracking.setFloodingNoExist(False)
            flows = FloodDetection.fDModule(packets, currSettings)
            data = Tracking.tracker(flows, currSettings, timeStart, timeEnd, db, cur)

            if data == None:
                timeStart = ''
                timeEnd = ''
                packets = []
                flows = []

            else:
                print (len(data[5]))
                #currSettings = StatControl.updateThreshold(data,currSettings)
                if Tracking.getFloodingNoExist(): Preprocessor.setFloodingEvent(False)
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
