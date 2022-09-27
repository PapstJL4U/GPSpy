"""my little client"""
import socket

class client():

    def __init__(self):

        self.socky = socket.socket()
        self.port = 12345
        self.num1 = 31
        self.num2 = 42
        self.sign ="-"
    def start(self):

        msg = f'{self.num1},{self.sign},{self.num2}'
        print(msg)
        bmsg = msg.encode(encoding="utf-8")
        self.socky.connect(('127.0.0.1', self.port))
        self.socky.send(bmsg)
        print("Encoding answer:"+self.socky.recv(1024).decode())
        #self.socky.close()
