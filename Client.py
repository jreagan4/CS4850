import socket
import struct

MCAST_GROUP = ('224.2.34.56', 5555)
BUFF_SIZE = 1024
MESSAGE = "This did not work"

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # this is magic socket library stuff, just go with it\

def sendMessage():
    MESSAGE = input("Enter message: ")
    if MESSAGE is '':
       sendMessage()
    else:
        soc.sendto(MESSAGE.encode('utf-8'), MCAST_GROUP)

def recieveMessage():
    data, addr = soc.recvfrom(BUFF_SIZE)
    print(data.decode('utf-8'))

def startConn():
    soc.settimeout(0.3)  # sets timeout so we don't block forever
    ttl = struct.pack('b',
                      1)  # sets time to live to 1 hop for local testing, need to change this later, format for windows to not be dumb
    soc.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)  # set socket options, also magic


    while 1:
        sendMessage()
        recieveMessage()
        """
        .encode() is important here, as sockets can only deal with bit-objects
        utf-8 makes the data decode as a string object
        """

try:
    startConn()

finally:
    print("disconnecting")
    soc.close()
