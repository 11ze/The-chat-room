import socket
import threading

IP = ''
PORT = 50007

words = { 'how are you?' : 'fine, thank you.',
          'how old are you?' : '38',
          'what is your name?' : 'Huang Dafeng',
          'what\'s your name?' : 'Huang Dafeng',
          'bye' : 'Bye'
        }

def tcp_connect(conn, addr):
    print('Connected by: ', addr)
    while True:
        data = conn.recv(1024)
        data = data.decode()
        print('Received message from {0}: {1}'.format( addr, data) )
        conn.send( words.get(data,'nothing').encode() )
        if data == 'bye':
            print('Disconnected from {0}'.format( addr ))
            break
    conn.close()

def main():
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    s.bind( (IP, PORT) )
    s.listen(3)
    print('tcp server is running...')

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=tcp_connect, args=(conn, addr))
        t.start()
    s.close()

main()
