class packet:

    def __init__(self,sourceIP,destIP,sourceMAC,destMAC,protocol,service,size):
        self.sourceIP = sourceIP
        self.destIP = destIP
        self.sourceMAC = sourceMAC
        self.destMAC = destMAC
        self.protocol = protocol
        self.service = service
        self.size = size

