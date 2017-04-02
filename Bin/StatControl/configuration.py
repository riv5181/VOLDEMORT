class adminSettings:
    maxTime = 10 # measured in seconds
    device = 'ens33' # network port that will be used
    network = '192.168.0.0/16' # network that will not be used for analysis (your own network)
    maxFlows = 50 # Number of expected flows to enter system. If exceeded, event is considered DDoS
    #Note: Thresholds manually configured will be set as the minimum threshold (new one will never go below given value)
    tcpThreshold = 60.00 # percentage with other thresholds; total with other thresholds should be 100, conversion of usage aleready done w/ BW
    udpThreshold = 25.00 # percentage with other thresholds; total with other thresholds should be 100, conversion of usage aleready done w/ BW
    icmpThreshold = 15.00 # percentage with other thresholds; total with other thresholds should be 100, conversion of usage aleready done w/ BW
    synThresh = 20.00 # percentage with other services under TCP; total with other TCP services should != 100, reserve for others not covered
    synackThresh = 20.00 # percentage with other services under TCP; total with other TCP services != 100, reserve for others not covered
    httpThresh = 50.00 # percentage with other services under TCP; total with other TCP services != 100, reserve for others not covered
    dnsThresh = 40.00 # percentage with other services under UDP; total with other UDP services != 100, reserve for others not covered
    dhcpThresh = 40.00 # percentage with other services under UDP; total with other UDP services != 100, reserve for others not covered
    tcplimit = 40.00 #Minimum possible threshold for TCP; Calculated values may never go beyond the given number
    udplimit = 15.00 #Minimum possible threshold for UDP; Calculated values may never go beyond the given number
    icmplimit = 5.00 #Minimum possible threshold for ICMP; Calculated values may never go beyond the given number
    #BW is multiplied to how many seconds, then get the 90% of it, since others are used for other protocols not covered
    bandwidth = (1250000 * maxTime) * 0.9 #Bandwidth of the network multiplied with measurement only used. Measured in bytes.
    cycle_time = 3
