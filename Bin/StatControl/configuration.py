class adminSettings:
    maxTime = 300 # measured in seconds
    device = 'ens33' # network port that will be used
    tcpThreshold = 50 # percentage with other thresholds; total with other thresholds should be 100
    udpThreshold = 30 # percentage with other thresholds; total with other thresholds should be 100
    icmpThreshold = 20 # percentage with other thresholds; total with other thresholds should be 100
    overallThreshold = 30 # threshold for all the protocols involved
    bandwidth = 10000000 #Bandwidth of the network. Measured in bytes. Use router interface bandwidth.
    cycle_time = 0
    tbwidth_util = 0
    suspicion_counter = 0
    set_prior_prot = 0
    suspicion_reset_counter = 0
