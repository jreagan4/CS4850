import socket
import struct

"""
packet loss against host, if host < threshold test all connections for better stability
if too many host swaps occur, stop host swapping for x amount of time
"""

MCAST_GRP = '224.2.34.56'
SERV_ADDR = ('', 5555)

BUFF_SIZE = 1024

def start_soc():
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.bind(SERV_ADDR)
        GRP = socket.inet_aton(MCAST_GRP)
        MREQ = struct.pack('4sL', GRP, socket.INADDR_ANY)
        soc.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, MREQ)
        return soc

def run():
    soc = start_soc()
    while 1:
        data, addr = soc.recvfrom(BUFF_SIZE)
        print("Data from ", addr) # server-side showing that we recieved something
        


if __name__ == '__main__':
    run()
