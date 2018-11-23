import socket
import threading
import time
import os
import os.path
import json    #用于将列表或字典转换成json字符串传输

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
        print('Received message from {0}: {1}'.format(addr, data))
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
    # 如果没有指定下载的文件则给客户端返回False
    if name in os.listdir() and '.' in name:
        conn.send('ok!'.encode())
        fileName = r'./' + name
        with open(fileName, 'rb') as f:    
            while True:
                a = f.read(1024)
                if not a:
                    break
                conn.send(a)
        time.sleep(0.1)  # 延时确保文件发送完整
        conn.send('EOF'.encode())
        print('文件发送完成!')
    else:
        conn.send('False'.encode())

# 保存上传的文件到当前工作目录
def recvFile(message):
    name = message.split()[1] #获取文件名
    fileName = r'./' + name
    print('开始保存!')
    with open(fileName, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if data == 'EOF'.encode():
                print('保存成功!')
                break
            f.write(data)

# 发送当前工作目录
def pwd():
    path = os.getcwd()
    conn.send(path.encode())

# 切换工作目录
def cd(message):
    message = message.split()[1]  # 截取目录名
    # 如果目录不存在或不是..则报错
    if not message in os.listdir():
        if message != '..':
            conn.send('False2'.encode())
            return
    if '.' in message:
        if message != '..':
            conn.send('False1'.encode())
            return
    f = r'./' + message
    os.chdir(f)
    pwd()

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

