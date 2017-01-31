import protCounterSM, deltaFlowSM

flows2 = []
floodedFlows = []
sPackets = []

def fDModule(packets, settings):
    global flows2
    sPackets = protCounterSM.segregatePackets(packets)

    flows2 = deltaFlowSM.createFlows(flows2, sPackets[0])
    flows2 = deltaFlowSM.createFlows(flows2, sPackets[1])
    flows2 = deltaFlowSM.createFlows(flows2, sPackets[2])
    #floodedFlows = deltaFlowSM.filterFlows(flows2, settings)

    maxi = len(flows2)
    i = 0
    while i < maxi:
        print (flows2[i].protocol)
        print (flows2[i].service + " " + flows2[i].pktFlag)
        print (flows2[i].sourceIP + "->" + flows2[i].destIP)
        print (flows2[i].datasize)
        print (" ")
        i = i + 1

    return floodedFlows





