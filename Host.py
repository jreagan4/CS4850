import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5555
BUFF_SIZE = 20

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((TCP_IP, TCP_PORT)) # bind the port to our program
soc.listen(10) # allows for 10 connections
conn, addr = soc.accept() # accept connecting sockets

while True:
        print("connected address: ", addr)
        data = conn.recv(BUFF_SIZE)
        if data: # print data if recieved data, otherwise do nothing for the noise in between data passes
            print("received data: ", data.decode('utf-8'))
