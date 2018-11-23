import socket

IP = ''
PORT = 50007

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.bind( (IP, PORT) )
s.listen(1)
print('tcp server is running...')

conn, addr = s.accept()
print('Connected by: ', addr)
data = conn.recv(1024)
data = data.decode()
print('Received message:', data)
conn.send( 'hello'.encode() )

conn.close()
s.close()
