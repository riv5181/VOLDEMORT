import sys
import thread
import Preprocessor
from classes import packet as thePacket


def main(argv):
    Preprocessor.obtainPackets()
    packets = Preprocessor.getCollectedPackets()
    print(str(len(packets)))

if __name__ == "__main__":
    main(sys.argv)