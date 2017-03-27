from classes import settings as Settings
import sys

ThresholdList = []  # this list is the thresholds
LimitList = []  # these are the lower limits
OriginalList = []  # un edited List
MasterHitList = []  # this is the tracker for each protocol
qwe = []
asd = []
zxc = []
MasterHitList.append(qwe)
MasterHitList.append(asd)
MasterHitList.append(zxc)

StateList = [0, 0, 0]
BooleanList = []
a_BList = [0, 0, 0]
b_BList = [0, 0, 0]
c_BList = [0, 0, 0]
BooleanList.append(a_BList)
BooleanList.append(b_BList)
BooleanList.append(c_BList)
currData = []
OriginalList = ThresholdList
loopTester = 0

def intializeValues():
    global ThresholdList, LimitList, OriginalList, MasterHitList, BooleanList, StateList, currData, OriginalList
    global loopTester
    ThresholdList = []  # this list is the thresholds
    LimitList = []  # these are the lower limits
    OriginalList = []  # un edited List
    MasterHitList = []  # this is the tracker for each protocol
    qwe = []
    asd = []
    zxc = []
    MasterHitList.append(qwe)
    MasterHitList.append(asd)
    MasterHitList.append(zxc)

    StateList = [0, 0, 0]
    BooleanList = []
    a_BList = [0, 0, 0]
    b_BList = [0, 0, 0]
    c_BList = [0, 0, 0]
    BooleanList.append(a_BList)
    BooleanList.append(b_BList)
    BooleanList.append(c_BList)
    currData = []
    OriginalList = ThresholdList
    loopTester = 0

def pht(list):
    sum = 0
    for numbers in list:
        sum += numbers
    ave = sum / (len(list))
    if (len(list) != 0):
        ave = sum / (len(list))
        return (ave)
    else:
        return 0


def getNeededBW(list, Value, IndexOfData):  # Value is the caculated data needed
    return Value - list[IndexOfData]


def getNeededBW2(list, Value, IndexOfData):  # Value is the caculated data needed
    return list[IndexOfData] - Value


def getFloodingAdjustment(list, IndexOfdata, NeededBW, Original):  # Adjusts The Value of The BW
    global ThresholdList, LimitList, StateList
    if (IndexOfdata == 0):
        if (list[2] - NeededBW >= LimitList[2] and StateList[2] != 1):
            ThresholdList[0] += NeededBW
            ThresholdList[2] -= NeededBW
        elif (list[2] - LimitList[2] >= 0 and StateList[2] != 1):
            currentAvailable = list[IndexOfdata] - LimitList[2]
            NeededBW = NeededBW - currentAvailable
            ThresholdList[0] += currentAvailable
            ThresholdList[2] -= currentAvailable
        else:
            print("No More bw Available 1.1")
        if (list[1] - NeededBW >= LimitList[1] and StateList[1] != 1):
            ThresholdList[0] += NeededBW
            ThresholdList[1] -= NeededBW
        elif (list[1] - LimitList[1] >= 0 and StateList[1] != 1):
            currentAvailable = list[1] - LimitList[1]
            NeededBW = NeededBW - currentAvailable
            ThresholdList[0] += currentAvailable
            ThresholdList[1] -= currentAvailable
        else:
            print("No More bw Available 1.2")

    elif (IndexOfdata == 1):
        if (list[2] - NeededBW >= LimitList[2] and StateList[2] != 1):
            ThresholdList[1] += NeededBW
            ThresholdList[2] -= NeededBW
        elif (list[2] - LimitList[2] >= 0 and StateList[2] != 1):
            currentAvailable = list[2] - LimitList[2]
            NeededBW = NeededBW - currentAvailable
            ThresholdList[1] += currentAvailable
            ThresholdList[2] -= currentAvailable
        else:
            print("No More bw Available 2.1")
        if (list[0] - NeededBW >= LimitList[0] and StateList[0] != 1):
            ThresholdList[1] += NeededBW
            ThresholdList[0] -= NeededBW
        elif (list[0] - LimitList[0] >= 0 and StateList[0] != 1):
            currentAvailable = list[0] - LimitList[0]
            NeededBW = NeededBW - currentAvailable
            ThresholdList[1] += currentAvailable
            ThresholdList[0] -= currentAvailable
        else:
            print("No More bw Available 2.2")

    elif (IndexOfdata == 2):
        if (list[1] - NeededBW >= LimitList[1] and StateList[1] != 1):
            ThresholdList[2] += NeededBW
            ThresholdList[1] -= NeededBW
        elif (list[1] - LimitList[1] >= 0 and StateList[1] != 1):
            currentAvailable = list[1] - LimitList[1]
            NeededBW = NeededBW - currentAvailable
            ThresholdList[2] += currentAvailable
            ThresholdList[1] -= currentAvailable
        else:
            print("No More bw Available 3.1")
        if (list[0] - NeededBW >= LimitList[0] and StateList[0] != 1):
            ThresholdList[2] += NeededBW
            ThresholdList[0] -= NeededBW
        elif (list[0] - LimitList[0] >= 0 and StateList[0] != 1):
            currentAvailable = list[0] - LimitList[0]
            NeededBW = NeededBW - currentAvailable
            ThresholdList[2] += currentAvailable
            ThresholdList[0] -= currentAvailable
        else:
            print("No More bw Available 3.2")

def getBackAdjustment(list, IndexOfdata, NeededBW, Original):  # Adjusts The Value of The BW
    global ThresholdList
    if (IndexOfdata == 0):
        if (list[1] < Original[1]):
            ThresholdList[2] += NeededBW
            ThresholdList[0] -= NeededBW

        elif (list[2] < Original[2]):
            ThresholdList[2] += NeededBW
            ThresholdList[0] -= NeededBW

    elif (IndexOfdata == 1):
        if (list[0] < Original[0]):
            ThresholdList[0] += NeededBW
            ThresholdList[1] -= NeededBW

        elif (list[2] < Original[2]):
            ThresholdList[2] += NeededBW
            ThresholdList[1] -= NeededBW

    elif (IndexOfdata == 2):
        if (list[0] < Original[0]):
            ThresholdList[0] += NeededBW
            ThresholdList[2] -= NeededBW

        elif (list[1] < Original[1]):
            ThresholdList[1] += NeededBW
            ThresholdList[2] -= NeededBW

def setInitStateList(list):  # Adjusts The Value of The BW
    global OriginalList, StateList
    if (list[0] > OriginalList[0]):
        StateList[0] = 1
    else:
        StateList[0] = 0
    if (list[1] > OriginalList[1]):
        StateList[1] = 1
    else:
        StateList[1] = 0
    if (list[2] > OriginalList[2]):
        StateList[2] = 1
    else:
        StateList[2] = 0

def updateThreshold(data, currSettings, adminSettings, db, cur):
    global ThresholdList, LimitList, MasterHitList, BooleanList, currData, loopTester
    newSettings = Settings('','','','','','','','','','','','','','','','','')
    currData = []

    intializeValues()

    ThresholdList.append(int(currSettings.tcpThreshold))
    ThresholdList.append(int(currSettings.udpThreshold))
    ThresholdList.append(int(currSettings.icmpThreshold))
    LimitList.append(int(currSettings.tcplimit))
    LimitList.append(int(currSettings.udplimit))
    LimitList.append(int(currSettings.icmplimit))

    setattr(newSettings, 'maxTime', currSettings.maxTime)
    setattr(newSettings, 'device', currSettings.device)
    setattr(newSettings, 'network', currSettings.network)
    setattr(newSettings, 'bandwidth', currSettings.bandwidth)
    setattr(newSettings, 'cycle_time', currSettings.cycle_time)
    setattr(newSettings, 'maxFlows', currSettings.maxFlows)
    setattr(newSettings, 'tcplimit', currSettings.tcplimit)
    setattr(newSettings, 'udplimit', currSettings.udplimit)
    setattr(newSettings, 'icmplimit', currSettings.icmplimit)

    # Take note of assigned IDs: 0 = TCP; 1 = UDP; 2 = ICMP
    currData.append(pht(data[0]))
    currData.append(pht(data[1]))
    currData.append(pht(data[2]))

    if (loopTester == 0):
        loopTester = 1
        setInitStateList(currData)

    if currData[0] < adminSettings.tcplimit and currData[1] < adminSettings.udplimit \
        and currData[2] < adminSettings.icmplimit:
        setattr(newSettings, 'tcpThreshold', float("%.2f" % adminSettings.tcpThreshold))
        setattr(newSettings, 'udpThreshold', float("%.2f" % adminSettings.udpThreshold))
        setattr(newSettings, 'icmpThreshold', float("%.2f" % adminSettings.icmpThreshold))
        # '''
        cur.execute("SELECT MAX(idcycle) FROM cycle")
        obtainedcurID = cur.fetchall()
        curID = int(obtainedcurID[0][0])

        cur.execute("INSERT INTO threshold (idcycle,old_tcp,old_udp,old_icmp,new_tcp,new_udp,new_icmp) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)", (curID, currSettings.tcpThreshold, currSettings.udpThreshold,
                                                            currSettings.icmpThreshold,
                                                            float("%.2f" % adminSettings.tcpThreshold),
                                                            float("%.2f" % adminSettings.udpThreshold),
                                                            float("%.2f" % adminSettings.icmpThreshold)))
        db.commit()
        # '''

    else:
        for x in range(0, 3):
            if (currData[x] > ThresholdList[x]):
                if (BooleanList[x][0] == 1 or BooleanList[x][2] == 0):
                    MasterHitList[x].append(currData[x])
                    BooleanList[x][2] += 1

                elif (BooleanList[x][0] == 0 and BooleanList[x][2] >= 1):
                    MasterHitList[x] = []
                    BooleanList[x][2] = 1
                    MasterHitList[x].append(currData[x])
                else:
                    BooleanList[x][2] = 0
                    MasterHitList[x] = []
                BooleanList[x][0] = 1
                BooleanList[x][1] = 0

            elif (currData[x] < ThresholdList[x]):
                if (BooleanList[x][1] == 1 or BooleanList[x][2] == 0):
                    MasterHitList[x].append(currData[x])
                    BooleanList[x][2] += 1
                elif (BooleanList[x][1] == 0 and BooleanList[x][2] >= 1):
                    MasterHitList[x] = []
                    BooleanList[x][2] = 1
                    MasterHitList[x].append(currData[x])
                else:
                    BooleanList[x][2] = 0
                    MasterHitList[x] = []
                BooleanList[x][0] = 0
                BooleanList[x][1] = 1

            if (BooleanList[x][0] == 1):
                StateList[x] = 1
                NeededBW = getNeededBW(ThresholdList, pht(MasterHitList[x]), x)
                getFloodingAdjustment(ThresholdList, x, NeededBW, OriginalList)
                MasterHitList[x] = []
                BooleanList[x][2] = 0

            elif (BooleanList[x][1] == 1):
                StateList[x] = 0
                NeededBW = getNeededBW2(ThresholdList, pht(MasterHitList[x]), x)
                getBackAdjustment(ThresholdList, x, NeededBW, OriginalList)
                MasterHitList[x] = []
                BooleanList[x][2] = 0


        if ThresholdList[2] > currSettings.icmplimit:
            if currData > currSettings.udpThreshold:
                value = currSettings.icmpThreshold - currSettings.icmplimit
                ThresholdList[0] = currSettings.tcpThreshold + value
                ThresholdList[1] = currSettings.udpThreshold
                ThresholdList[2] = currSettings.icmpThreshold - value

            else:
                value1 = currSettings.udpThreshold - currSettings.udplimit
                value2 = currSettings.icmpThreshold - currSettings.icmplimit
                ThresholdList[0] = currSettings.tcpThreshold + value1 + value2
                ThresholdList[1] = currSettings.udpThreshold - value1
                ThresholdList[2] = currSettings.icmpThreshold - value2

        setattr(newSettings, 'tcpThreshold', float("%.2f" % ThresholdList[0]))
        setattr(newSettings, 'udpThreshold', float("%.2f" % ThresholdList[1]))
        setattr(newSettings, 'icmpThreshold', float("%.2f" % ThresholdList[2]))

        #'''
        cur.execute("SELECT MAX(idcycle) FROM cycle")
        obtainedcurID = cur.fetchall()
        curID = int(obtainedcurID[0][0])

        cur.execute("INSERT INTO threshold (idcycle,old_tcp,old_udp,old_icmp,new_tcp,new_udp,new_icmp) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)", (curID, currSettings.tcpThreshold, currSettings.udpThreshold,
                    currSettings.icmpThreshold, float("%.2f" % ThresholdList[0]), float("%.2f" % ThresholdList[1]),
                    float("%.2f" % ThresholdList[2])))
        db.commit()
        #'''

    setattr(newSettings, 'synThresh', currSettings.synThresh)
    setattr(newSettings, 'synackThresh', currSettings.synackThresh)
    setattr(newSettings, 'httpThresh', currSettings.httpThresh)
    setattr(newSettings, 'dnsThresh', currSettings.dnsThresh)
    setattr(newSettings, 'dhcpThresh', currSettings.dhcpThresh)

    return newSettings
















