from classes import flow as theFlow

allFlows = []

def createFlows(flows, packets):
    j = 0
    maxj = len(flows)

    while j < maxj:
        i = 0
        maxi = len(packets)
        found = False

        while i < maxi:
            if flows[i].sourceIP == packets[j].sourceIP and flows[i].destIP == packets[j].destIP:
                if packets[j].protocol == 'TCP':
                    if flows[i].pktFlag == packets[j].pktFlag or flows[i].protocol == packets[j].protocol:
                        found = True
                        flows[i].datasize = flows[i].datasize + packets[j].size
                        i = i + 1

                    else:
                        i = i + 1

                elif packets[j].protocol == 'UDP':
                    if flows[i].protocol == packets[j].protocol:
                        found = True
                        flows[i].datasize = flows[i].datasize + packets[j].size
                        i = i + 1

                    else:
                        i = i + 1

                else:
                    found = True
                    flows[i].datasize = flows[i].datasize + packets[j].size
                    i = i + 1

            else:
                i = i + 1

        if found == False or len(flows) == 0:
            tempFlow = theFlow('', '', '', '', '', '', '')
            setattr(tempFlow, 'sourceIP', packets[j].sourceIP)
            setattr(tempFlow, 'destIP', packets[j].destIP)
            setattr(tempFlow, 'protocol', packets[j].protocol)
            setattr(tempFlow, 'service', packets[j].service)
            setattr(tempFlow, 'srcport', packets[i].srcport)
            setattr(tempFlow, 'destport', packets[i].destport)
            setattr(tempFlow, 'datasize', packets[i].size)
            print("OMGLOL")
            flows.append(tempFlow)

        j = j + 1

    print(str(len(flows)))
    return flows

def checkOverflow(flow, settings):
    tcpThresh = settings.bandwidth / settings.tcpThreshold
    udpThresh = settings.bandwidth / settings.udpThreshold
    icmpThresh = settings.bandwidth / settings.icmpThreshold
    tcpsynThresh = tcpThresh / settings.synThresh
    tcpsynackThresh = tcpThresh / settings.synackThresh
    tcphttpThresh = tcpThresh / settings.httpGETThresh
    udpdnsThresh = udpThresh / settings.dnsThresh
    udpdhcpThesh = udpThresh / settings.dhcpThresh

    if flow.protocol == 'TCP':
        if flow.pktFlag == 'SYN' and flow.datasize > tcpsynThresh:
            return True
        elif flow.pktFlag == 'SYN-ACK' and flow.datasize > tcpsynackThresh:
            return True
        elif flow.service == 'HTTP' and flow.datasize > tcphttpThresh:
            return True

    elif flow.protocol == 'UDP':
        if flow.service == 'DNS' and flow.datasize > udpdnsThresh:
            return True
        elif flow.service == 'DHCP' and flow.datasize > udpdhcpThesh:
            return True

    else:
        if flow.datasize > icmpThresh:
            return True

    return False

def filterFlows(flows, settings):
    floodedFlows = []
    i = 0
    maxi = len(flows)

    while i < maxi:
        if checkOverflow(flows[i], settings):
            floodedFlows.append(flows[i])

        i = i + 1
    
    return floodedFlows