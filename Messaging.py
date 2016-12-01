import pyaudio
import socket
import pickle
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sys
from multiprocessing import Process

ADDRESS = 'localhost'
TCP_PORT = 5555
BUFF_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 10240
app = QApplication(sys.argv)


qtCreatorFile = "GUI_V2.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

"""
Class definitions
    Payload for marshalling
    Client for receiving / sending data
    Server for hosting / routing data
"""


class Payload:
    # Payload marshals data for transfer, which is flattened by the client class
    def __init__(self, flag, data):
        self.flag = flag
        self.data = data

    def read(self):
        return self.flag

    def unload(self):
        return self.data


class Client:
    # contains send and receive methods, flattens received data
    linetext = ""
    
    def __init__(self):
        self.stream = pyaudio.PyAudio().open(format=FORMAT,
                                             channels=CHANNELS,
                                             rate=RATE,
                                             input=True,
                                             frames_per_buffer=BUFF_SIZE)
        self.mute = False
        self.started = False
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((ADDRESS, TCP_PORT))
        self.started = True
        print("connection made")

    def sendData(self, data):
        pdata = pickle.dumps(Payload(1, data.encode('utf-8')))
        print("data marshaled")
        self.soc.send(pdata)
        print("data away")

    def sendAudio(self):
        while 1:
            if not self.mute:
                try:
                    data = self.stream.read(BUFF_SIZE)
                    pdata = pickle.dumps(Payload(0, data))
                    self.soc.send(pdata)
                finally:
                    pass

    def readText(self, text):
        self.linetext = text.decode('utf-8')

    def readAudio(self, data):
        self.stream.write(data)
        self.soc.send('ACK'.encode('utf-8'))

    def receiveData(self):
        info, addr = self.soc.recvfrom(BUFF_SIZE)
        stuff = pickle.loads(info)
        if stuff.read() == 1:
            self.readText(stuff.unload())
        elif stuff.read() == 0:
            self.readAudio(stuff.unload())

    def run(self):
        self.sendAudio()
        print("started audio")
        self.receiveData()
        print("receiving data")

    def end(self):
        self.soc.close()

    def __exit__(self):
        self.end()


class Server:
    def __init__(self):
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.bind((ADDRESS, TCP_PORT))
        self.server_soc.listen(10)
        self.SOCKET_LIST = []
        # add server socket object to the list of readable connections
        self.SOCKET_LIST.append(self.server_soc)
        

    def findSoc(self):
        while 1:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self.server_soc.accept()
            self.SOCKET_LIST.append(client_address)
            # tester for connections
            print('connection from', client_address)

    def recvData(self):
        print("recvData invoked")
        while 1:
            for soc in self.SOCKET_LIST:
                data = soc.recv(BUFF_SIZE)
                if data:
                    print("server received data")
                    self.push_message(self.server_soc, data)

    def run(self):
        Process(target=self.findSoc)
        Process(target=self.recvData)

    # broadcast chat messages to all connected clients
    def push_message(self, server_soc, data):
        for socket in self.SOCKET_LIST:
            if socket != server_soc:
                try:
                    socket.send(data)
                    print("data pushed")
                except:
                    socket.close()
                    # remove unused sockets
                    if socket in self.SOCKET_LIST:
                        self.SOCKET_LIST.remove(socket)


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.client = None
        self.server = None
        self.line = None
        self.ui = Ui_MainWindow()
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.ui.setupUi(self)
        self.ui.sendButton.clicked.connect(self.handleSendButton)
        self.ui.createCallButton.clicked.connect(self.handleCreateButton)
        self.ui.addToCallButton.clicked.connect(self.handleJoinButton)
        Process(target=self.updateBox)


    def updateBox(self):
        while 1:
            if self.client.started == True:
                self.client.receiveData()

    def handleSendButton(self):
        TEST = ""
        MESSAGE = self.ui.chatInputBox.text()
        if MESSAGE == TEST:
            pass
        else:
            self.client.sendData(MESSAGE)
            self.ui.chatInputBox.clear()
            print("message away")


    def handleCreateButton(self):
        self.server = Server()
        Process(target=self.server.run)
        print("server started")

    def handleJoinButton(self):
        if self.server is None:
            print("no host present")
        if self.client is None:
            self.client = Client()
            Process(target=self.client.run)
            print("client made")
        else:
            print("connection exists")   

    def updateText(self):
        temp = self.client.getText()
        print("text received: ", temp)
        self.ui.chatBox.addItem(temp)


if __name__ == "__main__":
    window = MyApp()
    window.show()

sys.exit(app.exec_())

