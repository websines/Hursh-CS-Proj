#=================== MODULES ====================#
import socket
import _thread
import sys
import pygame
import pickle
from settings import Settings
vec = pygame.Vector2


class Server:

    def __init__(self, peers):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ''
        self.port = 1234
        self.server_ip = socket.gethostbyname(self.server)
        self.bind()
        self.peers = peers
        self.socket.listen(self.peers)
        self.settings = Settings()
        self.rects = []
        self.currentId = 0
        self.initRects()
        self.acceptRequest()

    def initRects(self):
        """ initialize rects here """
        self.rects = [(50,50),(100,100),(150,150)][:self.peers]

    def bind(self):
        try:
            self.socket.bind((self.server, self.port))
        except socket.error as err:
            print(str(err))

    def threadedClient(self,conn):
        myId = self.currentId
        conn.send(str.encode(str(self.currentId)))
        self.currentId += 1
        self.mainloop(conn, myId)

    def mainloop(self, conn, myId):
        running = True
        while running:
            try:
                data = conn.recv(2048)
                received = pickle.loads(data)
                print('received', received)
                if data:
                    self.rects[received[0]] = received[1] # id = vec
                    conn.sendall(pickle.dumps(self.rects))
                else:
                    conn.send(pickle.dumps(str(myId) + ' left the game'))
                    running = False
    
            except Exception as err:
                print(err)
                running = True

    def acceptRequest(self):
        print('waiting......')
        self.connections = []
        while True:
                conn,addr = self.socket.accept()
                self.connections.append((conn,addr))
                _thread.start_new_thread(self.threadedClient,(conn,))

if __name__ == "__main__":
    Server(2)

# received = [id, vec]