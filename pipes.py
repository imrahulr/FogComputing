# pipes.py

import socket

class pipes:

    soc =''
    typ = ''
    topic = ''

    def read_pipes(self, ):
        try:
            return self.soc.recv(16)
        except:
            self.set_connect()
            return self.soc.recv(16)

    def write_pipes(self, data):
        try:
            self.soc.send(data.encode('utf-8'))
        except:
            self.set_connect()
            self.soc.send(data.encode('utf-8'))

    def __init__(self, typ, topic):
        self.typ = typ
        self.topic = topic
        self.set_connect()

    def set_connect(self):
        self.soc = socket.socket()
        self.soc.connect(('127.0.0.1', 9009))
        try:
            msg = self.typ+'//'+self.topic
            self.soc.send(msg.encode('utf-8'))
        except:
            pass