import sys, socket

def getPacketsProtocol(oPackets, protocol):
    i = 0
    while i < len(oPackets):
        if oPackets[i].protocol != protocol:
            oPackets.remove(oPackets[i])
        i = i + 1
    return oPackets

def getTotalSize(oPackets)
    i = 0
    total = 0
    while i < len(oPackets):
        total = total + oPackets[i].size
        i = i + 1
    return total

def analyzePacketswThresh(oPackets, bandwidth, threshold):

    tcpPackets = getPacketsProtocol(oPackets,'TCP')
    udpPackets = getPacketsProtocol(oPackets, 'UDP')
    icmpPackets = getPacketsProtocol(oPackets, 'ICMP')

    tcpTotalSize = getTotalSize(tcpPackets)
    udpTotalSize = getTotalSize(udpPackets)
    icmpTotalSize = getTotalSize(icmpPackets)

    print ('BANDWIDTH: ' + bandwidth)
    print
    print ('TOTAL TCP SIZE: ' + tcpTotalSize)



    #Get network bandwidth then get average size of packets per protocol
    #Compare it with the bandwidth

    # just print it (For THSNE-2)
    #should return if protocol/s exceeded threshold??? (For THSNE-3)