import socket
from _thread import *
import sys
import pygame
import pickle
from settings import Settings
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 1234

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as err:
    print(str(err))

s.listen(2)

print('Waiting...')

currentID = 0
rects = []
settings = Settings()
for i in range(settings.num_of_players):
    rects.append((i*100 + 50,i*100 + 50))
key = False
def threaded_client(conn):
    global currentID, rects
    print('send id')
    conn.send(str.encode(str(currentID)))
    print('id sent')
    currentID += 1
    reply = rects
    # initial data can be sent here
    while True:
        try: # until something is received from conn
            data = conn.recv(2048)
            reply = pickle.loads(data) # [id,rect]
            if not data: # if data is empty... empty return
                conn.send(pickle.dumps('Good Bye!'))
                break # stop the thread for the conn
            else:
                print('Recieved: ',  reply)
                # process the reply
                rects[reply[0]] = reply[1]
                print('Sent: ' , rects)
                conn.sendall(pickle.dumps(rects))
        except Exception as err:
            print(err)
            break
    print('I got destroyed')


# the loop where the task proceed
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client,(conn,))
    

