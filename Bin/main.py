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

def getPackets():
    global packets, flows, currSettings, timeStart, timeEnd

    try:
        while True:
            timeStart = strftime("%m-%d-%Y %H:%M:%S", gmtime())
            packets = Preprocessor.obtainPackets(device1, maxTime1)

            print('BEFORE FILTER: ' + str(len(packets)))
            packets = Preprocessor.filterObtainedPackets(packets, mainIP, network)
            print('AFTER FILTER: ' + str(len(packets)))

            ifFlood = Preprocessor.analyzePacketswThresh(packets,currSettings)

            if ifFlood:
                timeEnd = strftime("%m-%d-%Y %H:%M:%S", gmtime())
                flows = FloodDetection.fDModule(packets, currSettings)
                data = Tracking.tracker(flows, currSettings, timeStart, timeEnd, db, cur)
                flows = []

                if data == 'NULL':
                    timeStart = ''
                    timeEnd = ''
                    packets = []

                else:
                    print (len(data[5]))
                    #currSettings = StatControl.updateThreshold(data,currSettings)
                    break

            else:
                flows = FloodDetection.fDModule(packets, currSettings)
                data = Tracking.tracker(flows, currSettings, timeStart, timeEnd, db, cur)
                flows = []

                if data == 'NULL':
                    timeStart = ''
                    timeEnd = ''
                    packets = []

                else:
                    print(len(data[5]))
                    # currSettings = StatControl.updateThreshold(data,currSettings)
                    break

    except KeyboardInterrupt:
        print('QUIT!')



thread1 = Thread(target = getPackets, args = ())
#thread2 = Thread(target = collectPackets, args = ())

thread1.start()
#thread2.start()

thread1.join()
#thread2.join()

db.close()
print (timeStart + " " + timeEnd)

#if __name__ == "__main__":
#    main(sys.argv)
