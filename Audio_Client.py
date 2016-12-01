import pyaudio
import socket

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 10240

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)


host = 'localhost'
port = 6666
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))


while 1:
    data = stream.read(chunk)
    s.send(data)
    s.recv(size)

s.close()
stream.close()
p.terminate()