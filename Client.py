import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5555
BUFF_SIZE = 1024
MESSAGE = "This did not work"

def setIP(ip):
       TCP_IP = ip

def setPort(port):
       TCP_PORT = port
        
def startConn(ip, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # this is magic socket library stuff, just go with it
    soc.connect((TCP_IP, TCP_PORT)) # connect to determined port and IP with our new socket object made from magic

    while 1:
    MESSAGE = input("Enter message: ")
    soc.send(MESSAGE.encode('utf-8'))
    """
    .encode() is important here, as sockets can only deal with bit-objects
    utf-8 makes the data decode as a string object
    """

startConn(TCP_IP, TCP_PORT)

soc.close()
