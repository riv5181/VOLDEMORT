class adminSettings:
    maxTime = 10 # measured in seconds
    device = 'ens33' # network port that will be used
    network = '192.168.0.0/16' # network that will not be used for analysis (your own network)
    maxFlows = 50 # Number of expected flows to enter system. If exceeded, event is considered DDoS
    #Note: Thresholds manually configured will be set as the minimum threshold (new one will never go below given value)
    tcpThreshold = 60.00 # percentage with other thresholds; total with other thresholds should be 100
    udpThreshold = 25.00 # percentage with other thresholds; total with other thresholds should be 100
    icmpThreshold = 15.00 # percentage with other thresholds; total with other thresholds should be 100
    synThresh = 25.00 # percentage with other services under TCP; total with other TCP services should be 100
    synackThresh = 25.00 # percentage with other services under TCP; total with other TCP services should be 100
    httpThresh = 50.00 # percentage with other services under TCP; total with other TCP services should be 100
    dnsThresh = 50.00 # percentage with other services under UDP; total with other UDP services should be 100
    dhcpThresh = 50.00 # percentage with other services under UDP; total with other UDP services should be 100
    tcplimit = 40.00 #Minimum possible threshold for TCP; Calculated values may never go beyond the given number
    udplimit = 15.00 #Minimum possible threshold for UDP; Calculated values may never go beyond the given number
    icmplimit = 10.00 #Minimum possible threshold for ICMP; Calculated values may never go beyond the given number
    bandwidth = 7500 #Bandwidth of the network. Measured in bytes. Use router interface bandwidth.
    cycle_time = 3
