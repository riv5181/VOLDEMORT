import sys, socket

def getPacketsProtocol(oPackets, protocol):
    i = 0
    while i < len(oPackets):
        if oPackets[i].protocol != protocol:
            oPackets.remove(oPackets[i])
        i = i + 1
    return oPackets

def getTotalDataSize(oPackets):
    i = 0
    total = 0
    while i < len(oPackets):
        total = total + oPackets[i].size
        i = i + 1
    return total

def calculateThreshold(totalThresh, threshPercentage):
    return totalThresh / threshPercentage

def printStatus(captured, threshold):
    if captured < threshold:
        return 'NORMAL'

    else:
        return 'ABNORMAL'

def analyzePacketswThresh(oPackets, currSettings):

    tcpPackets = getPacketsProtocol(oPackets,'TCP')
    udpPackets = getPacketsProtocol(oPackets, 'UDP')
    icmpPackets = getPacketsProtocol(oPackets, 'ICMP')

    tcpTotalDSize = getTotalDataSize(tcpPackets)
    udpTotalDSize = getTotalDataSize(udpPackets)
    icmpTotalDSize = getTotalDataSize(icmpPackets)

    tcpThresh = calculateThreshold(currSettings.bandwidth, currSettings.tcpThreshold)
    udpThresh = calculateThreshold(currSettings.bandwidth, currSettings.udpThreshold)
    icmpThresh = calculateThreshold(currSettings.bandwidth, currSettings.icmpThreshold)

    print ('BANDWIDTH: ' + currSettings.bandwidth + ' bytes')
    print
    print ('----- TCP INFORMATION-----')
    print ('THRESHOLD: ' + tcpThresh + ' bytes, (' + currSettings.tcpThreshold + '% of bandwidth)')
    print ('TOTAL CAPTURED TCP SIZE: ' + tcpTotalDSize)
    print ('STATUS: ' + printStatus(tcpTotalDSize,tcpThresh))
    print
    print('----- UDP INFORMATION-----')
    print('THRESHOLD: ' + udpThresh + ', bytes (' + currSettings.udpThreshold + '% of bandwidth)')
    print('TOTAL CAPTURED UDP SIZE: ' + udpTotalDSize)
    print('STATUS: ' + printStatus(udpTotalDSize, udpThresh))
    print
    print('----- ICMP INFORMATION-----')
    print('THRESHOLD: ' + icmpThresh + ', bytes (' + currSettings.icmpThreshold + '% of bandwidth)')
    print('TOTAL CAPTURED ICMP SIZE: ' + icmpTotalDSize)
    print('STATUS: ' + printStatus(icmpTotalDSize, icmpThresh))



    #Get network bandwidth then get average size of packets per protocol
    #Compare it with the bandwidth

    # just print it (For THSNE-2)
    #should return if protocol/s exceeded threshold??? (For THSNE-3)