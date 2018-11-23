'''
    既然要加入具有图形界面的聊天室中, 那么此文件服务器的客户端也需要有图形界面
    因为聊天室是之前的作业, 而且已经做好了大部分的基础操作
    这个客户端的图形界面化也算是再一次演示如何界面化的过程
    
    首先, 功能及处理:
        dir: 查看服务端文件夹里的文件和文件夹 -> 列表框实时显示
        get: 下载文件 -> 考虑在列表框的按钮添加此功能或者添加下载文件按钮
        cd : 进入文件夹 -> 考虑在列表框的按钮添加此功能或者添加切换文件夹按钮
        pwd: 服务端工作路径 -> 跟cd组合在一起
        put: 上传文件 -> 上传文件按钮
        quit: 断开连接 -> 考虑是否保留
        help: 查看可用命令 -> 去掉
        cls: 清屏 -> 去掉

    因为是在聊天室里加入此文件上传下载功能, 所以把登录(?)去掉了
    将main函数调用取消, 用鼠标的点击操作代替命令行的输入
    mian函数中有判断命令的if判断, 因为命令在点击时就已经确定,
    所以取消main函数没有影响
    添加窗口和显示路径和文件的组件

'''

import socket
import threading
import time
import os
import json    # 用于将列表或字典转换成json字符串传输
import tkinter
import tkinter.messagebox

IP = '127.0.0.1'
PORT2 = 50008    # 聊天室的端口为50007
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect((IP, PORT2))

## 创建窗口
ftp = tkinter.Tk()
ftp.title('文件')
ftp['height'] = 400
ftp['width'] = 300

# 创建标签显示服务端工作目录
lu = '显示路径'
label = tkinter.Label(ftp, text=lu)
label.place(x=5, y=0, )

# 创建列表框
list2 = tkinter.Listbox(ftp)
list2.place(x=5, y=20, width=290, height=330)

def main(): 
    while True:
        message = input('>>> ')
        if message == '':
            continue
        if message == 'quit':
            s.send(message.encode())
            break
        enter = message.split()[0]  # 获取命令的第一个参数(动作)
        ent_func(enter, message)
    s.close()

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

# 判断输入的命令并执行对应的函数
def ent_func(enter, message):
    if enter == 'get':
        return get(message)
    elif enter == 'put':
        return put(message)
    elif enter == 'dir':
        return recvList(enter)
    elif enter == 'pwd':
        return pwd(enter)
    elif enter == 'cd':
        return cd(enter, message)
    else:
        print('无效命令')

ftp.mainloop()
