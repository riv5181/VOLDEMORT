from classes import settings as Settings
import sys
import random
import time

def decideNewThresh(new, old):
    if int(new) > int(old):
        return int(new)

    else:
        return int(old)

def pht(list):
    sum = 0

    for numbers in list:
        sum += numbers

    ave = sum / (len(list))

    return (ave)

def updateThreshold(data, adminSettings):
    newSettings = Settings('','','','','','','','','','','','','')
    newThresholds = []

    setattr(newSettings, 'maxTime', adminSettings.maxTime)
    setattr(newSettings, 'device', adminSettings.device)
    setattr(newSettings, 'network', adminSettings.network)
    setattr(newSettings, 'bandwidth', adminSettings.bandwidth)
    setattr(newSettings, 'cycle_time', adminSettings.cycle_time)

    # Take note of assigned IDs: 0 = TCPSYN; 1 = TCPSYNACK; 2 = TCPHTTP; 3 = UDPDNS; 4 = UDPDHCP; 5 = ICMP
    # 6 = TCP; 7 = ICMP
    i = 0
    maxData = len(data)
    while i < maxData:
        newThresholds.append(pht(data[i]))
        i = i + 1

    setattr(newSettings, 'synThresh', decideNewThresh(newThresholds[0],adminSettings.synThresh))
    setattr(newSettings, 'synackThresh', decideNewThresh(newThresholds[1], adminSettings.synackThresh))
    setattr(newSettings, 'httpThresh', decideNewThresh(newThresholds[2], adminSettings.httpThresh))
    setattr(newSettings, 'dnsThresh', decideNewThresh(newThresholds[3], adminSettings.dnsThresh))
    setattr(newSettings, 'dhcpThresh', decideNewThresh(newThresholds[4], adminSettings.dhcpThresh))
    setattr(newSettings, 'icmpThreshold', decideNewThresh(newThresholds[5], adminSettings.icmpThreshold))
    setattr(newSettings, 'tcpThreshold', decideNewThresh(newThresholds[6], adminSettings.tcpThreshold))
    setattr(newSettings, 'udpThreshold', decideNewThresh(newThresholds[7], adminSettings.udpThreshold))

    return newSettings















