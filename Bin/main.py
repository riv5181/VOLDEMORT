import sys, socket, fcntl, struct, Preprocessor, StatControl
from threading import Thread
from classes import packet as thePacket


packets = []
device1 = StatControl.adminSettings.device
maxTime1 = StatControl.adminSettings.maxTime

def getPackets():
    global packets
    packets = Preprocessor.obtainPackets(device1, maxTime1)

    print('BEFORE FILTER: ' + str(len(packets)))
    Preprocessor.filterPackets(packets, device1)
    print('AFTER FILTER: ' + str(len(packets)))



def collectPackets():
    while (packets <= 0):
        print('NO PACKETS YET!')

    print(str(len(packets)))

thread1 = Thread(target = getPackets, args = ())
#thread2 = Thread(target = collectPackets, args = ())

thread1.start()
#thread2.start()

thread1.join()
#thread2.join()

#if __name__ == "__main__":
#    main(sys.argv)