import socket
from _thread import start_new_thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5555
BUFF_SIZE = 1024

def start_soc():
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind((TCP_IP, TCP_PORT))
        soc.listen(10)
        return soc

def socket_handler(client):
    while True:
        data = client.recv(BUFF_SIZE)
        if data :
            print("received data: ", data.decode('utf-8'))

def run():
    soc = start_soc()
    while 1:
        client, addr = soc.accept()
        print("connection from ", addr)
        start_new_thread(socket_handler, (client,))

if __name__ == '__main__':
    run()