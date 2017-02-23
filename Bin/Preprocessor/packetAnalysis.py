import sys, socket

tcpPackets = []
udpPackets = []
icmpPackets = []
floodEvent = False

def getFloodingEvent():
    return floodEvent

def setFloodingEvent(event):
    global floodEvent
    floodEvent = event

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

def analyzePacketswThresh(oPackets0, currSettings):
    global tcpPackets, udpPackets, icmpPackets, floodEvent
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
        floodEvent = True
        return True

    else:
        return False
