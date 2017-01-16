import protCounterSM

flows = []

def fDModule(packets):
    flows = protCounterSM.segregatePackets(packets)

    print(flows[0][0].protocol)
