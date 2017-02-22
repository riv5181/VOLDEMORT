from classes import flow as theFlow

#Creates flows per given list of packets
def createFlows(flows, packets):
    j = 0
    maxj = len(packets)

    while j < maxj:
        i = 0
        maxi = len(flows)
        found = False

        #analzes each flow if packet info matches flow info. If it does, add data size of packet to flow's size.
        while i < maxi:
            if flows[i].sourceIP == packets[j].sourceIP and flows[i].destIP == packets[j].destIP:
                if packets[j].protocol == 'TCP':
                    if flows[i].pktFlag == packets[j].flag or flows[i].service == packets[j].service:
                        found = True
                        flows[i].datasize = flows[i].datasize + packets[j].size
                        i = i + 1

                    else:
                        i = i + 1

                elif packets[j].protocol == 'UDP':
                    if flows[i].service == packets[j].service:
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

        #If flow is not found, create new one
        if found == False or len(flows) == 0:
            tempFlow = theFlow('', '', '', '', '', '', '', '','')
            setattr(tempFlow, 'sourceIP', packets[j].sourceIP)
            setattr(tempFlow, 'destIP', packets[j].destIP)
            setattr(tempFlow, 'protocol', packets[j].protocol)
            setattr(tempFlow, 'service', packets[j].service)
            setattr(tempFlow, 'srcport', packets[j].srcport)
            setattr(tempFlow, 'destport', packets[j].destport)
            setattr(tempFlow, 'pktFlag', packets[j].flag)
            setattr(tempFlow, 'datasize', packets[j].size)
            setattr(tempFlow, 'isFlood', False)
            print ('LOL')
            flows.append(tempFlow)

        j = j + 1

    return flows

#Simplified checker that can be used for IF statements. Just checks if total data size of flow is > than threshold
def checkOverflow(flow, settings):
    tcpThresh = settings.bandwidth * (settings.tcpThreshold * 0.01)
    udpThresh = settings.bandwidth * (settings.udpThreshold * 0.01)
    icmpThresh = settings.bandwidth * (settings.icmpThreshold * 0.01)
    tcpsynThresh = tcpThresh * (settings.synThresh * 0.01)
    tcpsynackThresh = tcpThresh * (settings.synackThresh * 0.01)
    tcphttpThresh = tcpThresh * (settings.httpGETThresh * 0.01)
    udpdnsThresh = udpThresh * (settings.dnsThresh * 0.01)
    udpdhcpThesh = udpThresh * (settings.dhcpThresh * 0.01)

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

#returns flows that are flooded
def filterFlows(flows, settings):
    i = 0
    maxi = len(flows)

    while i < maxi:
        if checkOverflow(flows[i], settings):
            flows[i].isFlood = True

        else:
            flows[i].isFlood = False

        i = i + 1
    
    return flows