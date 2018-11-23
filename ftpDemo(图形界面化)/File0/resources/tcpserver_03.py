import socket

IP = ''
PORT = 50007

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.bind( (IP, PORT) )
s.listen(3)
print('tcp server is running...')

while True:
    conn, addr = s.accept()
    print('Connected by: ', addr)
    data = conn.recv(1024)
    data = data.decode()
    print('Received message:', data)
    conn.send( 'hello\r\n'.encode() )
    if data == 'q':
        conn.close()
        print('Disconnected from {0}'.format( addr ))
        break

s.close()
