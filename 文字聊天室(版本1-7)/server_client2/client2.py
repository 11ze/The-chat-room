'''
    创建新线程来接收服务端发送的信息并打印出来
'''

import socket
import threading
import json

IP = '127.0.0.1'
PORT = 50007
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect( (IP, PORT) )

def main():
    print('Connected ...')
    while True:
        message = input('>>>')
        s.send( message.encode() )
        
        if message == 'bye':
            break
    s.close()

# 用于时刻接收服务端发送的信息并打印
def recv():
    while True:
        data = s.recv(1024)
        data = json.loads(data.decode())
        print(data)

r = threading.Thread(target=recv)
r.start()

m = threading.Thread(target=main)
m.start()

