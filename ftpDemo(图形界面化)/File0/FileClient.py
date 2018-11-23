'''
    登录名: ftp  密码: 空
    服务端起始工作目录为resource文件夹
    get 文件名:下载文件到download文件夹, 如果文件已存在, 可选择是否覆盖
    put 文件名: 上传客户端所在的指定文件到服务端工作目录下
    cd 目录名 or ..: 进入或返回上一文件夹
    dir: 显示当前目录所有文件和目录名
    help: 可用命令  quit: 断开连接  cls: 清屏

'''

import socket
import threading
import time
import os
import json    #用于将列表或字典转换成json字符串传输

IP = '127.0.0.1'
PORT = 50008
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect((IP, PORT))

def main(): 
    user = input('user: ')
    pwd = input('password: ')
    if pwd == '' and user == 'ftp':
        while True:
            message = input('>>> ')
            if message == '':
                continue
            if message == 'quit':
                s.send(message.encode())
                break
            enter = message.split()[0]  # 获取命令的第一个参数(动作)
            ent_func(enter, message)
            
    else:
        input('用户名或密码错误!')
        main()
    s.close()



# 输入help或命令有误时显示(help)
def helpList():
    print('''
get: 下载\tput: 上传\thelp: 可用命令
quit: 断开连接\tcd: 进入文件夹\tdir: 当前目录
cls: 清屏''')

# 接收下载文件(get)
def get(message):
    name = message.split()
    if len(name) != 2:
        return print('请输入文件名') 
    name = name[1]  # 获取命令的第二个参数(文件名)
    # 判断是否已下载该文件
    if name in os.listdir(r'./download'):
        while True:
            ch = input('文件已存在是否覆盖[Y/N]:')
            if ch == 'Y' or ch == 'y':
                break
            elif ch == 'N' or ch == 'n':
                print('取消下载')
                return
            else:
                continue
    # 判断服务端是否有指定下载的文件, 没有则报错
    s.send(message.encode())
    data = s.recv(1024)
    if data.decode() == 'False':
        print('没有该文件')
        return
    fileName = r'./download/' + name
    print('开始下载文件!')
    with open(fileName, 'wb') as f:
        while True:
            data = s.recv(1024)
            if data == 'EOF'.encode():
                print('下载完成!')
                break
            f.write(data)

# 上传客户端所在文件夹中指定的文件到服务端
def put(message):
    name = message.split()
    if len(name) != 2:
        return print('请输入文件名')
    name = name[1]  # 获取文件名
    # 判断 Upload 目录中是否有该文件
    if not name in os.listdir():
        print('没有该文件')
        return
    if '.' not in name:
        print('请输入正确的文件名!')
        return
    s.send(message.encode())
    fileName = r'./' + name
    print('开始上传文件!')
    with open(fileName, 'rb') as f:
        while True:
            a = f.read(1024)
            if not a:
                break
            s.send(a)
        time.sleep(0.1)  # 延时确保文件发送完整
        s.send('EOF'.encode())
        print('文件上传成功')

# 将接收到的目录文件列表打印出来(dir)
def recvList(enter):
    s.send(enter.encode())
    data = s.recv(1024)
    data = json.loads(data.decode())
    for i in range(len(data)):
        print(data[i-1])

# 打印服务端当前工作目录(pwd)
def pwd(enter):
    s.send(enter.encode())
    data = s.recv(1024)
    print(data.decode())

# 进入指定目录(cd)
def cd(enter, message):
    s.send(message.encode())
    data = s.recv(1024).decode()
    if data == 'False1':
        print('请输入正确的目录名')
        return
    if data == 'False2':
        print('没有该目录!')
        return
    print(data)

# 清屏, 命令行下有效(cls)
def cls():
    os.system('cls')

# 判断输入的命令并执行对应的函数
def ent_func(enter, message):
    if enter == 'help':
        return helpList()
    elif enter == 'get':
        return get(message)
    elif enter == 'put':
        return put(message)
    elif enter == 'dir':
        return recvList(enter)
    elif enter == 'pwd':
        return pwd(enter)
    elif enter == 'cd':
        return cd(enter, message)
    elif enter == 'cls':
        return cls()
    else:
        print('无效命令')
       
main()
