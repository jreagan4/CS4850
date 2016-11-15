import socket
import struct
import threading

MCAST_ADDR = '224.2.34.56'
MCAST_GRP = ('224.2.34.56', 5555)
SERV_ADDR = ('', 5555)
BUFF_SIZE = 1024
MESSAGE = "This did not work"


def start_soc():
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind(SERV_ADDR)
    GRP = socket.inet_aton(MCAST_ADDR)
    MREQ = struct.pack('4sL', GRP, socket.INADDR_ANY)
    soc.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, MREQ)
    return soc

def sendMessage(soc):
    MESSAGE = input("Enter message: ")
    if MESSAGE is '':
        recieveMessage(soc)
    else:
        soc.sendto(MESSAGE.encode('utf-8'), MCAST_GRP)

def recieveMessage(soc):
    while 1:
        try:
            data, addr = soc.recvfrom(BUFF_SIZE)
            while data:
                if not data:
                    break
                print(data.decode('utf-8'))
                data, addr = soc.recvfrom(BUFF_SIZE)
        except socket.timeout:
            sendMessage(soc)

def startConn(soc):
    soc.settimeout(0.3)  # sets timeout so we don't block forever
    ttl = struct.pack('b',
                      1)  # sets time to live to 1 hop for local testing, need to change this later, format for windows to not be dumb
    soc.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)  # set socket options, also magic


    threading.Thread(target=recieveMessage(soc), args=[soc]).start()


try:
    soc = start_soc()
    startConn(soc)


finally:
    print("disconnecting")
