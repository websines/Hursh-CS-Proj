import socket
import threading

s = socket.socket()

port = 12345

s.connect(('127.0.0.1',port))
def send_text(s):
    while True:
        a = input()
        if a == 'exit':
            break
        s.send(bytes(a,'utf-8'))
def recieve_text(s,a):
    while True:
        print(s.recv(1024))
        if input() == 'x':
            break

#t = threading.Thread(target = send_text,args = (s,))
v = threading.Thread(target = recieve_text,args = (s,2))
#t.start()
v.start()
v.join()
s.close()
