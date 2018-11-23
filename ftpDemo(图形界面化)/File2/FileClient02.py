'''
    创建一个窗口, 添加显示服务端工作路径的标签和显示文件和文件夹的列表框
    然后对pwd和recvList函数稍加修改, 将原来的print换成显示在标签和列表框

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

# 创建列表框
list2 = tkinter.Listbox(ftp)
list2.place(x=5, y=20, width=290, height=330)

# 将接收到的目录文件列表打印出来(dir), 显示在列表框中
def recvList(enter):
    s.send(enter.encode())
    data = s.recv(1024)
    data = json.loads(data.decode())
    list2.delete(0, tkinter.END)  # 清空列表框
    list2.insert(tkinter.END, ' ..')
    for i in range(len(data)):
        list2.insert(tkinter.END, (' '+data[i]))

# 打印服务端当前工作目录(pwd)
def pwd(enter):
    s.send(enter.encode())
    data = s.recv(1024)
    recvList('dir')
    return data.decode()  # 返回接收到的路径

# 创建标签显示服务端工作目录
lu = pwd('pwd')
label = tkinter.Label(ftp, text=lu)
label.place(x=5, y=0, )

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
main()
