import socket

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 1234

        self.addr = (self.host, self.port)
        self.id = int(self.connect())

    def connect(self):
        # connect self to self.addr
        self.client.connect(self.addr)
        return self.client.recv(2048).decode() #id


    def send(self, data):
        try:
            self.client.send(data)
            reply = self.client.recv(2048)
            return reply
        except Exception as err:
            print(str(err))

