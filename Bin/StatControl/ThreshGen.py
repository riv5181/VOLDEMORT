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

BooleanList = []
a_BList = [0, 0, 0]
b_BList = [0, 0, 0]
c_BList = [0, 0, 0]
BooleanList.append(a_BList)
BooleanList.append(b_BList)
BooleanList.append(c_BList)
currData = []
OriginalList = ThresholdList

def intializeValues():
    global ThresholdList, LimitList, OriginalList, MasterHitList, BooleanList, currData, OriginalList
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

    BooleanList = []
    a_BList = [0, 0, 0]
    b_BList = [0, 0, 0]
    c_BList = [0, 0, 0]
    BooleanList.append(a_BList)
    BooleanList.append(b_BList)
    BooleanList.append(c_BList)
    currData = []
    OriginalList = ThresholdList

def pht(list):
    sum = 0
    for numbers in list:
        sum += numbers
    ave = sum / (len(list))
    return (ave)


def getNeededBW(list, Value, IndexOfData):  # Value is the caculated data needed
    return Value - list[IndexOfData]


def getNeededBW2(list, Value, IndexOfData):  # Value is the caculated data needed
    return list[IndexOfData] - Value


def getFloodingAdjustment(list, IndexOfdata, NeededBW, Original):  # Adjusts The Value of The BW
    global ThresholdList
    if (IndexOfdata == 0):
        if (list[2] - NeededBW >= LimitList[2]):
            ThresholdList[0] += NeededBW
            ThresholdList[2] -= NeededBW

        elif (list[1] - NeededBW >= LimitList[1]):
            ThresholdList[0] += NeededBW
            ThresholdList[1] -= NeededBW

        else:
            print("No More bw Available 1")

    elif (IndexOfdata == 1):
        if (list[2] - NeededBW >= LimitList[2]):
            ThresholdList[1] += NeededBW
            ThresholdList[2] -= NeededBW

        elif (list[0] - NeededBW >= LimitList[0]):
            ThresholdList[1] += NeededBW
            ThresholdList[0] -= NeededBW

        else:
            print("No More bw Available 2")

    elif (IndexOfdata == 2):
        if (list[1] - NeededBW >= LimitList[1]):
            ThresholdList[2] += NeededBW
            ThresholdList[1] -= NeededBW

        elif (list[0] - NeededBW >= LimitList[0]):
            ThresholdList[2] += NeededBW
            ThresholdList[0] -= NeededBW

        else:
            print("No More bw Available 3")

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

def updateThreshold(data, adminSettings, db, cur):
    global ThresholdList, LimitList, MasterHitList, BooleanList, currData
    newSettings = Settings('','','','','','','','','','','','','','','','','')
    currData = []

    #intializeValues()

    ThresholdList.append(int(adminSettings.tcpThreshold))
    ThresholdList.append(int(adminSettings.udpThreshold))
    ThresholdList.append(int(adminSettings.icmpThreshold))
    LimitList.append(int(adminSettings.tcplimit))
    LimitList.append(int(adminSettings.udplimit))
    LimitList.append(int(adminSettings.icmplimit))

    setattr(newSettings, 'maxTime', adminSettings.maxTime)
    setattr(newSettings, 'device', adminSettings.device)
    setattr(newSettings, 'network', adminSettings.network)
    setattr(newSettings, 'bandwidth', adminSettings.bandwidth)
    setattr(newSettings, 'cycle_time', adminSettings.cycle_time)
    setattr(newSettings, 'maxFlows', adminSettings.maxFlows)
    setattr(newSettings, 'tcplimit', adminSettings.tcplimit)
    setattr(newSettings, 'udplimit', adminSettings.udplimit)
    setattr(newSettings, 'icmplimit', adminSettings.icmplimit)

    # Take note of assigned IDs: 0 = TCP; 1 = UDP; 2 = ICMP
    currData.append(pht(data[0]))
    currData.append(pht(data[1]))
    currData.append(pht(data[2]))

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
            NeededBW = getNeededBW(ThresholdList, pht(MasterHitList[x]), x)
            getFloodingAdjustment(ThresholdList, x, NeededBW, OriginalList)
            MasterHitList[x] = []
            BooleanList[x][2] = 0

        elif (BooleanList[x][1] == 1):
            NeededBW = getNeededBW2(ThresholdList, pht(MasterHitList[x]), x)
            getBackAdjustment(ThresholdList, x, NeededBW, OriginalList)
            MasterHitList[x] = []
            BooleanList[x][2] = 0

    setattr(newSettings, 'tcpThreshold', float("%.2f" % ThresholdList[0]))
    setattr(newSettings, 'udpThreshold', float("%.2f" % ThresholdList[1]))
    setattr(newSettings, 'icmpThreshold', float("%.2f" % ThresholdList[2]))

    cur.execute("SELECT MAX(idcycle) FROM cycle")
    obtainedcurID = cur.fetchall()
    curID = int(obtainedcurID[0][0])

    cur.execute("INSERT INTO threshold (idcycle,old_tcp,old_udp,old_icmp,new_tcp,new_udp,new_icmp) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)", (curID,adminSettings.tcpThreshold,adminSettings.udpThreshold,
                adminSettings.icmpThreshold,float("%.2f" % ThresholdList[0]),float("%.2f" % ThresholdList[1]),
                float("%.2f" % ThresholdList[2])))
    db.commit()

    setattr(newSettings, 'synThresh', adminSettings.synThresh)
    setattr(newSettings, 'synackThresh', adminSettings.synackThresh)
    setattr(newSettings, 'httpThresh', adminSettings.httpThresh)
    setattr(newSettings, 'dnsThresh', adminSettings.dnsThresh)
    setattr(newSettings, 'dhcpThresh', adminSettings.dhcpThresh)
    return newSettings
















