import protCounterSM, deltaFlowSM

flows2 = []
floodedFlows = []
sPackets = []
numFlood = 0
flowBefore = 0
lenPackets = []

def getFlowBefore():
    return flowBefore

def getNumFloods():
    return numFlood

def getLenPackets():
    return lenPackets

def fDModule(packets, settings):
    global flows2, floodedFlows, sPackets, lenPackets, numFlood, flowBefore
    floodedFlows = []
    flows2 = []
    numFlood = 0
    lenPackets = []
    sPackets = protCounterSM.segregatePackets(packets)

    lenPackets.append(len(sPackets[0]))
    lenPackets.append(len(sPackets[1]))
    lenPackets.append(len(sPackets[2]))

    #This segment searches for the priority protocol (Highest Threshold). It will be analyzed first for flows.
    if len(sPackets[0]) > len (sPackets[1]) and len(sPackets[0]) > len (sPackets[2]):
        flows2 = deltaFlowSM.createFlows(flows2, sPackets[0])
        if len(sPackets[1]) > len (sPackets[2]):
            flows2 = deltaFlowSM.createFlows(flows2, sPackets[1])
        else:
            flows2 = deltaFlowSM.createFlows(flows2, sPackets[2])

    elif len(sPackets[1]) > len (sPackets[0]) and len(sPackets[1]) > len (sPackets[2]):
        flows2 = deltaFlowSM.createFlows(flows2, sPackets[1])
        if len(sPackets[0]) > len (sPackets[2]):
            flows2 = deltaFlowSM.createFlows(flows2, sPackets[0])
        else:
            flows2 = deltaFlowSM.createFlows(flows2, sPackets[2])

    else:
        flows2 = deltaFlowSM.createFlows(flows2, sPackets[2])
        if len(sPackets[0]) > len(sPackets[1]):
            flows2 = deltaFlowSM.createFlows(flows2, sPackets[0])
        else:
            flows2 = deltaFlowSM.createFlows(flows2, sPackets[1])

    maxi = len(flows2)
    flowBefore = maxi
    i = 0

    while i < maxi:
        print(flows2[i].protocol)
        print(flows2[i].service + " " + flows2[i].pktFlag)
        print(flows2[i].sourceIP + "->" + flows2[i].destIP)
        print(flows2[i].datasize)
        print(" ")
        i = i + 1

    #Calls fucntion for finding which flows are flooded
    floodedFlows = deltaFlowSM.filterFlows(flows2, settings)

    maxi = len(floodedFlows)
    i = 0
    print('-------')
    print('FLOODED FLOWS: ')
    print('-------')
    while i < maxi:
        if floodedFlows[i].isFlood == True:
            print(floodedFlows[i].protocol)
            print(floodedFlows[i].service + " " + floodedFlows[i].pktFlag)
            print(floodedFlows[i].sourceIP + "->" + floodedFlows[i].destIP)
            print(floodedFlows[i].datasize)
            print(" ")
            numFlood = numFlood + 1

        i = i + 1

    return floodedFlows





