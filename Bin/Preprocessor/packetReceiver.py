import socket, pcapy, sys, time, datetime
from struct import *
from classes import packet as thePacket

packets = []
finalpackets = []
startTime = time.time()
currentTime = 0

def obtainPackets(device, maxTime):
    global startTime, currentTime, packets

    '''
    open device
    # Arguments here are:
    #   device
    #   snaplen (maximum number of bytes to capture _per_packet_)
    #   promiscious mode (1 for true)
    #   timeout (in milliseconds)

    '''
    cap = pcapy.open_live(device, 65536, 1, 0)

    # start sniffing packets
    while (currentTime < maxTime):
        (header, packet) = cap.next()
        # print ('%s: captured %d bytes, truncated to %d bytes' %(datetime.datetime.now(), header.getlen(), header.getcaplen()))
        parse_packet(packet)

        currentTime = int(time.time() - startTime)
        print
        print('TOTAL CAPTURED PACKETS:' + str(len(packets)))
        print('ELAPSED: ' + str(currentTime))
        print

    return packets

# Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr(a):
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]), ord(a[1]), ord(a[2]), ord(a[3]), ord(a[4]), ord(a[5]))
    return b

# function to parse a packet
def parse_packet(packet):
    global packets
    tempPacket = thePacket('','','','','','','','')
    pktFlag = ''
    # parse ethernet header
    eth_length = 14

    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])
    print ('Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(
        eth_protocol))

    setattr(tempPacket,'sourceMAC',eth_addr(packet[6:12]))
    setattr(tempPacket, 'destMAC', eth_addr(packet[0:6]))

    # Parse IP packets, IP Protocol number = 8
    if eth_protocol == 8:
        # Parse IP header
        # take first 20 characters for the ip header
        ip_header = packet[eth_length:20 + eth_length]

        # now unpack them :)
        iph = unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = iph[0]
        packet_size = iph[2]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF

        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);

        print ('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(
            protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr))

        setattr(tempPacket, 'sourceIP', str(s_addr))
        setattr(tempPacket, 'destIP', str(d_addr))

        # TCP protocol
        if protocol == 6:
            t = iph_length + eth_length
            tcp_header = packet[t:t + 20]

            # now unpack them :)
            tcph = unpack('!HHLLBBHHH', tcp_header)

            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4] #tackle this for identifying if syn or syn0ack
            tcph_length = doff_reserved >> 4
            flag = tcph[5] #2 is SYN, 18 is SYN-ACK, 16 is ACK; urg, ack, psh, rst, syn, fin

            if flag == 2:
                pktFlag = 'SYN'

            elif flag == 18:
                pktFlag = 'SYN-ACK'

            #elif flag == 16:
                #pktFlag = 'ACK'

            else:
                pktFlag = 'OTHER'

            print ('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(
                sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length) +
                   ' ' + 'Flag : ' + pktFlag + ' PCKT : TCP')

            h_size = eth_length + iph_length + tcph_length * 4
            data_size = len(packet) + h_size #includes packet header size

            # get data from the packet
            data = packet[h_size:]

            print ('Data Size: ' + str(data_size) + ' bytes')

            setattr(tempPacket, 'protocol', 'TCP')
            setattr(tempPacket, 'service', str(dest_port))
            setattr(tempPacket, 'flag', str(pktFlag))
            setattr(tempPacket, 'size', data_size)
            packets.append(tempPacket)

        # ICMP Packets
        elif protocol == 1:
            u = iph_length + eth_length
            icmph_length = 4
            icmp_header = packet[u:u + 4]

            # now unpack them :)
            icmph = unpack('!BBH', icmp_header)

            icmp_type = icmph[0]
            code = icmph[1]
            checksum = icmph[2]

            print ('Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum) + ' PCKT: ICMP')

            h_size = eth_length + iph_length + icmph_length
            data_size = len(packet) + h_size

            # get data from the packet
            data = packet[h_size:]

            print ('Data Size: ' + str(data_size) + ' bytes')

            setattr(tempPacket, 'protocol', 'ICMP')
            setattr(tempPacket, 'service', 'ECHO-REPLY')
            setattr(tempPacket, 'flag', 'NULL')
            setattr(tempPacket, 'size', data_size)
            packets.append(tempPacket)

        # UDP packets
        elif protocol == 17:
            u = iph_length + eth_length
            udph_length = 8
            udp_header = packet[u:u + 8]

            # now unpack them :)
            udph = unpack('!HHHH', udp_header)

            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]

            print ('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(
                length) + ' Checksum : ' + str(checksum) + ' PCKT: UDP')

            h_size = eth_length + iph_length + udph_length
            data_size = len(packet) + h_size

            # get data from the packet
            data = packet[h_size:]
            serv = ''

            if dest_port == 53:
                serv = 'DNS'

            elif dest_port == 67 or dest_port == 68:
                serv = 'DHCP'

            else:
                serv = 'OTHER'

            print ('Data Size: ' + str(data_size) + ' bytes')

            setattr(tempPacket, 'protocol', 'UDP')
            setattr(tempPacket, 'service', serv)
            setattr(tempPacket, 'flag', 'NULL')
            setattr(tempPacket, 'size', data_size)
            packets.append(tempPacket)

        # some other IP packet like IGMP
        else:
            print ('Protocol other than TCP/UDP/ICMP')

        print


if __name__ == "__main__":
    main(sys.argv)