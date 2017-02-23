class adminSettings:
    maxTime = 10 # measured in seconds
    device = 'ens33' # network port that will be used
    network = '192.168.0.0/24' # network that will not be used for analysis (your own network)
    #Note: Thresholds manually configured will be set as the minimum threshold (new one will never go below given value)
    tcpThreshold = 50 # percentage with other thresholds; total with other thresholds should be 100
    udpThreshold = 30 # percentage with other thresholds; total with other thresholds should be 100
    icmpThreshold = 20 # percentage with other thresholds; total with other thresholds should be 100
    synThresh = 25 # percentage with other services under TCP; total with other TCP services should be 100
    synackThresh = 25 # percentage with other services under TCP; total with other TCP services should be 100
    httpThresh = 50 # percentage with other services under TCP; total with other TCP services should be 100
    dnsThresh = 50 # percentage with other services under UDP; total with other UDP services should be 100
    dhcpThresh = 50 # percentage with other services under UDP; total with other UDP services should be 100
    bandwidth = 2000 #Bandwidth of the network. Measured in bytes. Use router interface bandwidth.
    cycle_time = 3
