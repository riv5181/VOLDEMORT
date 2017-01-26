import protCounterSM, deltaFlowSM

flows1 = []
flows2 = []
floodedFlows = []
sPackets = []

def fDModule(packets, settings):
    sPackets = protCounterSM.segregatePackets(packets)
    flows2 = deltaFlowSM.createFlows(flows1, sPackets[0])
    flows2 = flows2 + flows1
    flows2 = deltaFlowSM.createFlows(flows1, sPackets[1])
    flows2 = flows2 + flows1
    flows2 = deltaFlowSM.createFlows(flows1, sPackets[2])
    flows2 = flows2 + flows1
    print(str(len(flows2)))
    floodedFlows = deltaFlowSM.filterFlows(flows2, settings)

    return floodedFlows





