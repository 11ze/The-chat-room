'''
    因为聊天室服务端和文件服务端的代码可以各自单独运行
    所以嵌套在一起很简单
    将两个服务端的代码都打包成函数(chatServer/fileServer)用线程各自单独运行
'''

import socket
import threading
import queue
import json  # json.dumps(some)打包   json.loads(some)解包
import time
import os
import os.path

def chatServer():
    IP = ''
    PORT = 50007

    que = queue.Queue()  # 用于存放客户端发送的信息的队列
    users = []  # 用于存放在线用户的信息  [conn, user, addr]
    lock = threading.Lock()  # 创建锁, 防止多个线程写入数据的顺序打乱

    # 用于接收所有客户端发送信息的函数
    def tcp_connect(conn, addr):
        # 连接后将用户信息添加到users列表
        user = conn.recv(1024)  # 接收用户名
        user = user.decode()
        if user == 'no':
            user = addr[0] + ':' + str(addr[1])
        users.append((conn, user, addr))
        print('新连接:', addr, ':', user, end='')  # 打印用户名
        d = onlines()  # 有新连接则刷新客户端的在线用户显示
        recv(addr, d)
        try:
            while True:
                data = conn.recv(1024)
                data = data.decode()
                recv(addr, data)  # 保存信息到队列
            conn.close()
        except:
            print(user + ' 断开连接')
            delUsers(conn, addr)  # 将断开用户移出users
            conn.close()

    # 判断断开用户在users中是第几位并移出列表, 刷新客户端的在线用户显示
    def delUsers(conn, addr):
        a = 0
        for i in users:
            if i[0] == conn:
                users.pop(a)
                print('剩余在线用户: ', end='')  # 打印剩余在线用户(conn)
                d = onlines()
                recv(addr, d)
                print(d)
                break
            a += 1

    # 将接收到的信息(ip,端口以及发送的信息)存入que队列
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
                data = ''
                message = que.get()  # 取出队列第一个元素
                if isinstance(message[1], str):  # 如果data是str则返回Ture
                    for i in range(len(users)):
                        #user[i][1]是用户名, users[i][2]是addr, 将message[0]改为用户名
                        for j in range(len(users)):
                            if message[0] == users[j][2]:                            
                                data = ' ' + users[j][1] + '：' + message[1]
                                break      
                        users[i][0].send(data.encode())
                data = data.split(':;')[0]
                print(data)
                if isinstance(message[1], list):  # 同上
                    # 如果是list则打包后直接发送  
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        users[i][0].send(data.encode())
                

    # 将在线用户存入online列表并返回
    def onlines():
        online = []
        for i in range(len(users)):
            online.append(users[i][1])
        return online
                    
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

################################################################
def fileServer():
    first = r'.\resources'
    os.chdir(first)  # 把first设为当前工作路径
    IP = ''
    PORT = 50008
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    s.bind( (IP, PORT) )
    s.listen(3)

    def tcp_connect(conn, addr):
        print('Connected by: ', addr)
        
        while True:
            data = conn.recv(1024)
            data = data.decode()
            if data == 'quit':
                print('Disconnected from {0}'.format(addr))
                break
            order = data.split()[0]  # 获取动作
            recv_func(order, data)
                
        conn.close()

    # 传输当前目录列表
    def sendList():
        listdir = os.listdir(os.getcwd())
        listdir = json.dumps(listdir)
        conn.sendall(listdir.encode())

    # 发送文件函数
    def sendFile(message):
        name = message.split()[1]  #获取第二个参数(文件名)
        fileName = r'./' + name
        with open(fileName, 'rb') as f:    
            while True:
                a = f.read(1024)
                if not a:
                    break
                conn.send(a)
        time.sleep(0.1)  # 延时确保文件发送完整
        conn.send('EOF'.encode())

    # 保存上传的文件到当前工作目录
    def recvFile(message):
        name = message.split()[1] #获取文件名
        fileName = r'./' + name
        with open(fileName, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if data == 'EOF'.encode():
                    break
                f.write(data)

    # 切换工作目录
    def cd(message):
        message = message.split()[1]  # 截取目录名
        # 如果是新连接或者下载上传文件后的发送则 不切换 只将当前工作目录发送过去
        if message != 'same':
            f = r'./' + message
            os.chdir(f)
        path = ''
        path = os.getcwd().split('\\')  # 当前工作目录 
        for i in range(len(path)):
            if path[i] == 'resources':
                break
        pat = ''
        for j in range(i, len(path)):
            pat = pat + path[j] + ' '
        pat = '\\'.join(pat.split())
        # 如果切换目录超出范围则退回切换前目录
        if not 'resources' in path:
            f = r'./resources'
            os.chdir(f)
            pat = 'resources'
        conn.send(pat.encode())

    # 判断输入的命令并执行对应的函数
    def recv_func(order, message):
        if order == 'get':
            return sendFile(message)
        elif order == 'put':
            return recvFile(message)
        elif order == 'dir':
            return sendList()
        elif order == 'pwd':
            return pwd()
        elif order == 'cd':
            return cd(message)

    print('tcp server is running...')
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=tcp_connect, args=(conn, addr))
        t.start()
    s.close()

serv1 = threading.Thread(target=chatServer)
serv1.start()
serv2 = threading.Thread(target=fileServer)
serv2.start()
