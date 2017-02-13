import sys, socket, fcntl, struct, Preprocessor, StatControl, FloodDetection, Tracking
from threading import Thread
from classes import packet as thePacket


packets = []
flows = []
data = []
currSettings = StatControl.adminSettings
device1 = StatControl.adminSettings.device
maxTime1 = StatControl.adminSettings.maxTime

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
    global packets, flows, currSettings

    try:
        while True:
            packets = Preprocessor.obtainPackets(device1, maxTime1)

            print('BEFORE FILTER: ' + str(len(packets)))
            packets = Preprocessor.filterObtainedPackets(packets, mainIP)
            print('AFTER FILTER: ' + str(len(packets)))

            ifFlood = Preprocessor.analyzePacketswThresh(packets,currSettings)

            if ifFlood:
                flows = FloodDetection.fDModule(packets, currSettings)
                data = Tracking.tracker(flows, currSettings)
                flows = []

                if data == 'NULL':
                    packets = []

                else:
                    print (len(data[5]))
                    #currSettings = StatControl.updateThreshold(data,currSettings)
                    break

            else:
                packets = [] #If there is no flooding, refresh obtained packets and collect again

    except KeyboardInterrupt:
        print('QUIT!')


thread1 = Thread(target = getPackets, args = ())
#thread2 = Thread(target = collectPackets, args = ())

thread1.start()
#thread2.start()

thread1.join()
#thread2.join()

#if __name__ == "__main__":
#    main(sys.argv)
