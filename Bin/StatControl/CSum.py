import sys
import random
import time
import math


def updateCurrentThreshold(list):
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


def CalculateThreshold(ThresholdList, LimitList, MasterHitList, BooleanList, IndexOfData, interval, currData, counter):
    if (currData[IndexOfData] > ThresholdList[IndexOfData]):

        if (BooleanList[IndexOfData][0] == 1 or BooleanList[IndexOfData][2] == 0):
            MasterHitList[IndexOfData].append(currData[IndexOfData])
            BooleanList[IndexOfData][2] += 1

        elif (BooleanList[IndexOfData][0] == 0 and BooleanList[IndexOfData][2] >= 1):
            MasterHitList[IndexOfData] = []
            BooleanList[IndexOfData][2] = 1
            MasterHitList[IndexOfData].append(currData[IndexOfData])
        else:
            BooleanList[IndexOfData][2] = 0
            MasterHitList[IndexOfData] = []
        BooleanList[IndexOfData][0] = 1
        BooleanList[IndexOfData][1] = 0
    elif (currData[IndexOfData] < ThresholdList[IndexOfData]):
        if (BooleanList[IndexOfData][1] == 1 or BooleanList[IndexOfData][2] == 0):
            MasterHitList[IndexOfData].append(currData[IndexOfData])
            BooleanList[IndexOfData][2] += 1
        elif (BooleanList[IndexOfData][1] == 0 and BooleanList[IndexOfData][2] >= 1):
            MasterHitList[IndexOfData] = []
            BooleanList[IndexOfData][2] = 1
            MasterHitList[IndexOfData].append(currData[IndexOfData])
        else:
            BooleanList[IndexOfData][2] = 0
            MasterHitList[IndexOfData] = []
        BooleanList[IndexOfData][0] = 0
        BooleanList[IndexOfData][1] = 1
    if (counter >= interval and BooleanList[IndexOfData][0] == 1):
        NeededBW = getNeededBW(ThresholdList, updateCurrentThreshold(MasterHitList[IndexOfData]), IndexOfData)
        getFloodingAdjustment(ThresholdList, IndexOfData, NeededBW, OriginalList)
        MasterHitList[IndexOfData] = []
        BooleanList[IndexOfData][2] = 0
    elif (counter >= interval and BooleanList[IndexOfData][1] == 1):
        NeededBW = getNeededBW2(ThresholdList, updateCurrentThreshold(MasterHitList[IndexOfData]), IndexOfData)
        getBackAdjustment(ThresholdList, IndexOfData, NeededBW, OriginalList)
        MasterHitList[IndexOfData] = []
        BooleanList[IndexOfData][2] = 0


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

TCP = input('Enter TCP: ')
UDP = input('Enter UDP size: ')
ICMP = input('Enter ICMP size: ')
TCPLowerLimit = input('Enter TCP Lower Limit: ')
UDPLowerLimit = input('Enter UDP Lower Limit size: ')
ICMPLowerLimit = input('Enter ICMPLowerLimit Lower Limit: ')

# init_Threshold =input('Enter Your Threshold(Threshold for data to be considered as a possible attack')
# Threshold = init_Threshold
# Threshold = float(Threshold)

# lowerlimit = input('Enter you Lower Limit size(Minimun Value that the threshold can have')
# lowerlimit = int(lowerlimit)
# x = random.uniform(1, 100)

interval = input('Enter you Interval size(Number of hits before Threshold is recalculated)')
interval = int(interval)
counter = 0
TCP = int(TCP)
UDP = int(UDP)
ICMP = int(ICMP)
TCPLowerLimit = int(TCPLowerLimit)
UDPLowerLimit = int(UDPLowerLimit)
ICMPLowerLimit = int(ICMPLowerLimit)
ThresholdList.append(TCP)
ThresholdList.append(UDP)
ThresholdList.append(ICMP)
LimitList.append(TCPLowerLimit)
LimitList.append(UDPLowerLimit)
LimitList.append(ICMPLowerLimit)
BooleanList = []
a_BList = [0, 0, 0]
b_BList = [0, 0, 0]
c_BList = [0, 0, 0]
BooleanList.append(a_BList)
BooleanList.append(b_BList)
BooleanList.append(c_BList)
currData = []
OriginalList = ThresholdList

while (True):
    currData = []

    TCPList = [0, 0, 0];
    UDPList = [0, 0, 0];
    ICMPList = [random.uniform(1, 10), random.uniform(1, 100), random.uniform(1, 100)];
    currData.append(updateCurrentThreshold(TCPList))
    currData.append(updateCurrentThreshold(UDPList))
    currData.append(updateCurrentThreshold(ICMPList))

    time.sleep(3)
    print("New Data: ", currData[0])
    print("New Data: ", currData[1])
    print("New Data: ", currData[2])
    #  print ("Current Threshold: " ,Threshold )

    for x in range(0, 3):
        CalculateThreshold(ThresholdList, LimitList, MasterHitList, BooleanList, x, interval, currData, counter)
    if (counter >= 3):
        counter = 0
    counter += 1
    print(BooleanList)
    print(MasterHitList)
    print("TCP Thresh: " + str("%.2f" % ThresholdList[0]))
    print("UDP Thresh: " + str("%.2f" % ThresholdList[1]))
    print("ICMP Thresh: " + str("%.2f" % ThresholdList[2]))
    print("Total Thresh: " + str(float("%.2f" % ThresholdList[0]) + float("%.2f" % ThresholdList[1]) + float("%.2f" % ThresholdList[2])))





