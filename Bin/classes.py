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

#Assigns the flow class. Contains necessary stuff in a flow to be analyzed.
class flow:

    def __init__(self,sourceIP,destIP,protocol,service,srcport,destport,pktFlag,datasize,isFlood):
        self.sourceIP = sourceIP
        self.destIP = destIP
        self.protocol = protocol
        self.service = service
        self.srcport = srcport
        self.destport = destport
        self.pktFlag = pktFlag
        self.datasize = datasize
        self.isFlood = isFlood

#Assigns the new settings class. Will contain the new thresholds that will be used
class settings:

    def __init__(self,maxTime,device,network,maxFlows,tcpThreshold,udpThreshold,icmpThreshold,synThresh,synackThresh,
                 httpThresh,dnsThresh,dhcpThresh,bandwidth,cycle_time):
        self.maxTime = maxTime
        self.device = device
        self.network = network
        self.maxFlows = maxFlows
        self.tcpThreshold = tcpThreshold
        self.udpThreshold = udpThreshold
        self.icmpThreshold = icmpThreshold
        self.synThresh = synThresh
        self.synackThresh = synackThresh
        self.httpThresh = httpThresh
        self.dnsThresh = dnsThresh
        self.dhcpThresh = dhcpThresh
        self.bandwidth = bandwidth
        self.cycle_time = cycle_time

