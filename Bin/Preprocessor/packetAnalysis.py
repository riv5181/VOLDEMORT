import sys, socket

tcpPackets = []
udpPackets = []
icmpPackets = []

def getPacketsProtocol(oPackets1):
    global tcpPackets, udpPackets, icmpPackets
    i = 0
    max = len(oPackets1)

    while i < max:
        if oPackets1[i].protocol == 'TCP':
            tcpPackets.append(oPackets1[i])

        elif oPackets1[i].protocol == 'UDP':
            udpPackets.append(oPackets1[i])

        elif oPackets1[i].protocol == 'ICMP':
            icmpPackets.append(oPackets1[i])

        i = i + 1

def getTotalDataSize(oPackets2):
    i = 0
    total = 0
    while i < len(oPackets2):
        total = total + oPackets2[i].size
        i = i + 1
    return total

def calculateThreshold(totalThresh, threshPercentage):
    return 0.01 * (int(totalThresh) * int(threshPercentage))
'''
def printStatus(captured, threshold1):
    if int(captured) < int(threshold1):
        return 'NORMAL'

    else:
        return 'ABNORMAL'

def analyzePacketswThresh(oPackets0, currSettings):
    global tcpPackets, udpPackets, icmpPackets

    getPacketsProtocol(oPackets0)

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
'''
def analyzePacketswThresh(oPackets0, currSettings):
    global tcpPackets, udpPackets, icmpPackets
    tcpPackets = []
    udpPackets = []
    icmpPackets = []

    getPacketsProtocol(oPackets0)

    tcpTotalDSize = getTotalDataSize(tcpPackets)
    udpTotalDSize = getTotalDataSize(udpPackets)
    icmpTotalDSize = getTotalDataSize(icmpPackets)

    tcpThresh = calculateThreshold(currSettings.bandwidth, currSettings.tcpThreshold)
    udpThresh = calculateThreshold(currSettings.bandwidth, currSettings.udpThreshold)
    icmpThresh = calculateThreshold(currSettings.bandwidth, currSettings.icmpThreshold)

    if tcpTotalDSize > tcpThresh or udpTotalDSize > udpThresh or icmpTotalDSize > icmpThresh:
        return True

    else:
        return False
