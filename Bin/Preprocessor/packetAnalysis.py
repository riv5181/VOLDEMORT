import sys, socket

def getPacketsProtocol(oPackets1, protocol1):
    i = 0
    max = len(oPackets1)

    while i < max:
        if oPackets1[i].protocol != protocol1:
            oPackets1.remove(oPackets1[i])

        max = len(oPackets1)
        i = i + 1

    return oPackets1

def getTotalDataSize(oPackets2):
    i = 0
    total = 0
    while i < len(oPackets2):
        total = total + oPackets2[i].size
        i = i + 1
    return total

def calculateThreshold(totalThresh, threshPercentage):
    return int(totalThresh) / int(threshPercentage)

def printStatus(captured, threshold1):
    if int(captured) < int(threshold1):
        return 'NORMAL'

    else:
        return 'ABNORMAL'

def analyzePacketswThresh(oPackets0, currSettings):

    tcpPackets = getPacketsProtocol(oPackets0,'TCP')
    udpPackets = getPacketsProtocol(oPackets0, 'UDP')
    icmpPackets = getPacketsProtocol(oPackets0, 'ICMP')

    tcpTotalDSize = getTotalDataSize(tcpPackets)
    udpTotalDSize = getTotalDataSize(udpPackets)
    icmpTotalDSize = getTotalDataSize(icmpPackets)

    tcpThresh = calculateThreshold(currSettings.bandwidth, currSettings.tcpThreshold)
    udpThresh = calculateThreshold(currSettings.bandwidth, currSettings.udpThreshold)
    icmpThresh = calculateThreshold(currSettings.bandwidth, currSettings.icmpThreshold)

    print ('BANDWIDTH: ' + str(currSettings.bandwidth) + ' bytes')
    print
    print ('----- TCP INFORMATION-----')
    print ('THRESHOLD: ' + str(tcpThresh) + ' bytes, (' + str(currSettings.tcpThreshold) + '% of bandwidth)')
    print ('PACKETS CAPTURED: ' + str(len(tcpPackets)))
    print ('TOTAL CAPTURED TCP SIZE: ' + str(tcpTotalDSize) + ' bytes')
    print ('STATUS: ' + str(printStatus(tcpTotalDSize,tcpThresh)))
    print
    print('----- UDP INFORMATION-----')
    print('THRESHOLD: ' + str(udpThresh) + ', bytes (' + str(currSettings.udpThreshold) + '% of bandwidth)')
    print('PACKETS CAPTURED: ' + str(len(udpPackets)))
    print('TOTAL CAPTURED UDP SIZE: ' + str(udpTotalDSize) + ' bytes')
    print('STATUS: ' + str(printStatus(udpTotalDSize, udpThresh)))
    print
    print('----- ICMP INFORMATION-----')
    print('THRESHOLD: ' + str(icmpThresh) + ', bytes (' + str(currSettings.icmpThreshold) + '% of bandwidth)')
    print('PACKETS CAPTURED: ' + str(len(icmpPackets)))
    print('TOTAL CAPTURED ICMP SIZE: ' + str(icmpTotalDSize) + ' bytes')
    print('STATUS: ' + str(printStatus(icmpTotalDSize, icmpThresh)))



    #Get network bandwidth then get average size of packets per protocol
    #Compare it with the bandwidth

    # just print it (For THSNE-2)
    #should return if protocol/s exceeded threshold??? (For THSNE-3)