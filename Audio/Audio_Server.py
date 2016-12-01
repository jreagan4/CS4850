
import pyaudio
import socket

sock_list = []

def audio_init():
    """ Pyaudio Initialization """
    chunk = 1024
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
    # host = socket.gethostname()
    host = 'localhost'
    port = 50000
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
            for sock in sock_list:
                if sock == client:
                    pass
                else:
                    stream.write(data)  # Stream the recieved audio data
                    client.send('ACK'.encode('utf-8'))  # Send an ACK

def run():
    s = socket_init()
    while(1):
        client, address = s.accept()
        sock_list.append(client)
        print('Incoming connection')
        socket_handler(client)


if __name__=='__main__':
    run()
