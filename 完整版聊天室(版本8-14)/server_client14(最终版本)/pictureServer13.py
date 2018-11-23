import socket
import threading
import time
import os
import os.path
import json

################################################################
def pictureServer():
    IP = ''
    PORT = 50009    # 再开一个端口运行此图片缓存服务器
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    s.bind( (IP, PORT) )
    s.listen(5)

    def tcp_connect2(conn, addr):
        while True:
            data = conn.recv(1024)
            data = data.decode()
            print('Received message from {0}: {1}'.format(addr, data))
            if data == 'quit':
                break
            order = data.split()[0]  # 获取动作
            recv_func2(order, data)        
        conn.close()
        print('---')
    folder = './服务端图片缓存/'    # 图片的保存文件夹
    # 发送文件函数
    def sendFile2(message):
        print(message)
        name = message.split()[1]  #获取第二个参数(文件名)
        fileName = folder + name   # 将文件夹和图片名连接起来
        with open(fileName, 'rb') as f:    
            while True:
                a = f.read(1024)
                if not a:
                    break
                conn.send(a)
        time.sleep(0.1)  # 延时确保文件发送完整
        conn.send('EOF'.encode())
        print('文件发送完成!')

    # 保存上传的文件到当前工作目录
    def recvFile2(message):
        print(message)
        name = message.split()[1] #获取文件名
        fileName = folder + name   # 将文件夹和图片名连接起来
        print('开始保存!')
        with open(fileName, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if data == 'EOF'.encode():
                    print('保存成功!')
                    break
                f.write(data)

    # 判断输入的命令并执行对应的函数
    def recv_func2(order, message):
        if order == 'get':
            return sendFile2(message)
        elif order == 'put':
            return recvFile2(message)

    print('开始运行...')
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=tcp_connect2, args=(conn, addr))
        t.start()
    s.close()    


serv3 = threading.Thread(target=pictureServer)
serv3.start()

