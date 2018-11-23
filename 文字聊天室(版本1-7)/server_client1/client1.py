'''

'''

import socket
import threading

IP = '127.0.0.1'
PORT = 50007

def main():
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    s.connect( (IP, PORT) )
    print('Connected ...')

    while True:
        message = input('>>>')
        s.send( message.encode() )
        data = s.recv(1024)
        data = data.decode()
        print( data )
        if message == 'bye':
            break
    s.close()

main()
