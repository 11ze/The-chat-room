'''
    用第二个线程将que中所有的信息发给连接到的所有客户端
'''

import socket
import threading
import queue
import json  # json.dumps(some)打包   json.loads(some)解包

IP = ''
PORT = 50007

que = queue.Queue()  # 用于存放客户端发送的信息
users = []  # 用于存放在线用户
lock = threading.Lock()  # 创建锁, 防止多个线程写入数据的顺序打乱

# 用于接收所有客户端发送信息的函数
def tcp_connect(conn, addr):
    users.append(conn)
    print('新连接: ', addr)
    try:
        while True:
            data = conn.recv(1024)
            data = data.decode()
            #conn.send( 'hello\r\n'.encode() )
            recv(addr, data)  # 保存信息
        conn.close()
    except:
        print('断开了')
        delUsers(conn)
        conn.close()

# 判断断开用户在users中是第几位并移出列表
def delUsers(conn):
    a = 0
    for i in users:
        if i == conn:
            users.pop(a)
            print('剩余在线用户: ', users)  # 打印剩余在线用户(conn)
            return
        a += 1

    
# 将接收到的信息(ip,端口以及发送的信息)存入message列表
def recv(addr, data):
    lock.acquire()
    try:
        que.put((addr, data))
    finally:
        lock.release()

# 将队列que中的消息发送给所有连接到的用户
def sendData():
    while True:
        if not que.empty():
            message = list(que.get())
            print(message)
            message = json.dumps(message)
            for i in range(len(users)):
                users[i].send(message.encode())

def main():
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    s.bind( (IP, PORT) )
    s.listen(5)
    print('tcp server is running...')
    q = threading.Thread(target=sendData)
    q.start()
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=tcp_connect, args=(conn, addr))
        t.start()
    s.close()

main()
