class adminSettings:
    maxTime = 10 # measured in seconds
    device = 'ens33' # network port that will be used
    network = '192.168.0.0/24' # network that will not be used for analysis (your own network)
    tcpThreshold = 50 # percentage with other thresholds; total with other thresholds should be 100
    udpThreshold = 30 # percentage with other thresholds; total with other thresholds should be 100
    icmpThreshold = 20 # percentage with other thresholds; total with other thresholds should be 100
    #overallThreshold = 30 # threshold for all the protocols involved
    synThresh = 25 # percentage with other services under TCP; total with other TCP services should be 100
    synackThresh = 25 # percentage with other services under TCP; total with other TCP services should be 100
    httpGETThresh = 25 # percentage with other services under TCP; total with other TCP services should be 100
    httpPOSThresh = 25 # percentage with other services under TCP; total with other TCP services should be 100
    dnsThresh = 50 # percentage with other services under UDP; total with other UDP services should be 100
    dhcpThresh = 50 # percentage with other services under UDP; total with other UDP services should be 100
    bandwidth = 1000 #Bandwidth of the network. Measured in bytes. Use router interface bandwidth.
    cycle_time = 3
    #tbwidth_util = 0
    #suspicion_counter = 0
    #set_prior_prot = 0
    #suspicion_reset_counter = 0
