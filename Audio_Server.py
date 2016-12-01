import pyaudio
import socket
from multiprocessing import Process


def audio_init():
    """ Pyaudio Initialization """
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 10240
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True)
    return stream

def socket_init():
    """ Socket Initialization """
    host = 'localhost'
    port = 6666
    backlog = 5
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(backlog)
    return s

def socket_handler(client):
    size = 1024
    stream = audio_init()
    # Main Functionality
    while 1:
        data = client.recv(size)
        if data:
            # Write data to pyaudio stream
            stream.write(data)  # Stream the recieved audio data

def run():
    s = socket_init()
    while(1):
        client, address = s.accept()
        print('Incoming connection')
        Process(target=socket_handler(client)).start()


if __name__=='__main__':
    run()
