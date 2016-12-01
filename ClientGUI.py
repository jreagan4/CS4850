import sys
import socket
import struct
import threading
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyleFactory
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *

MCAST_ADDR = '224.2.34.56'
MCAST_GRP = ('224.2.34.56', 5555)
SERV_ADDR = ('', 5555)
BUFF_SIZE = 75
MESSAGE = ""

qtCreatorFile = "GUI_V2.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
soc = socket.socket                

def start_soc():
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind(SERV_ADDR)
    GRP = socket.inet_aton(MCAST_ADDR)
    MREQ = struct.pack('4sL', GRP, socket.INADDR_ANY)
    soc.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, MREQ)
    return soc

def startConn(soc):
    soc.settimeout(0.3)  # sets timeout so we don't block forever
    ttl = struct.pack('b',
                      1)  # sets time to live to 1 hop for local testing, need to change this later, format for windows to not be dumb
    soc.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)  # set socket options, also magic
    threading.Thread(target=recieveMessage(soc), args=[soc]).start() 

def getSoc():
    return soc

def createConn(soc): 
    try:
        soc = start_soc()
        startConn(soc)
    finally:
        print("disconnecting")
        
def sendMessage(soc):
    MESSAGE = input("")
    if MESSAGE is not '':
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
                

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui=Ui_MainWindow()
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.ui.setupUi(self)
        self.ui.sendButton.clicked.connect(self.handleSendButton)
        self.ui.addToCallButton.clicked.connect(self.handleAddToCallButton)
        self.ui.removeFromCallButton.clicked.connect(self.handleRemoveFromCallButton)
        self.ui.muteButton.clicked.connect(self.handleMuteButton)
        
    def updateText(self, text):
        self.ui.chatBox.addItem(text) 
           
    def handleSendButton(self):        
        MESSAGE = self.ui.chatInputBox.text()
        if MESSAGE is not '':
            self.ui.chatBox.addItem('Peter: ' +MESSAGE)
        self.ui.chatBox.scrollToBottom()
        self.ui.chatInputBox.clear()
    
    def handleMuteButton(self):
        self.ui.muteButton
        
    def handleAddToCallButton(self):  
        contactListCount = self.ui.contactList.count()
        if contactListCount > 0:        
            self.ui.currentCallList.addItem('Peter')
            #self.ui.contactsList.removeItemWidget(self.ui.contactsList.currentItem())
        
    def handleRemoveFromCallButton(self):
        currentCallCount = self.ui.currentCallList.count()
        if currentCallCount > 0:
            self.ui.contactList.addItem(self.ui.currentCallList.currentItem())
            self.ui.currentCallList.removeItemWidget(self.ui.currentCallList.currentItem())
    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
