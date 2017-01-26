#Assigns the packet class. Contains necessary stuff in a packet to be analyzed.
class packet:

    def __init__(self,sourceIP,destIP,sourceMAC,destMAC,protocol,service,srcport,destport,flag,size):
        self.sourceIP = sourceIP
        self.destIP = destIP
        self.sourceMAC = sourceMAC
        self.destMAC = destMAC
        self.protocol = protocol
        self.service = service
        self.srcport = srcport
        self.destport = destport
        self.flag = flag
        self.size = size

class flow:

    def __init__(self,sourceIP,destIP,protocol,service,srcport,destport,pktFlag,datasize):
        self.sourceIP = sourceIP
        self.destIP = destIP
        self.protocol = protocol
        self.service = service
        self.srcport = srcport
        self.destport = destport
        self.pktFlag = pktFlag
        self.datasize = datasize

