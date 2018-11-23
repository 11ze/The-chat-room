'''
    将保存文件功能使用选择对话框设置保存路径和名字
    将列表框的显示上添加颜色
    同时也删除一些多余的判断, 如判断已存在是否覆盖

'''

import socket
import threading
import time
import os
import json    # 用于将列表或字典转换成json字符串传输
import tkinter
import tkinter.messagebox
from tkinter import filedialog    # 用于弹出选择对话框

IP = '127.0.0.1'
PORT2 = 50008    # 聊天室的端口为50008
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect((IP, PORT2))
label = ''# 显示路径的标签

## 创建窗口
ftp = tkinter.Tk()
ftp.title('文件')
ftp['height'] = 400
ftp['width'] = 300

# 创建列表框
list2 = tkinter.Listbox(ftp)
list2.place(x=5, y=20, width=290, height=330)

# 将接收到的目录文件列表打印出来(dir), 显示在列表框中, 在pwd函数中调用
def recvList(enter):
    s.send(enter.encode())
    data = s.recv(4096)  
    data = json.loads(data.decode())
    list2.delete(0, tkinter.END)  # 清空列表框
    list2.insert(tkinter.END, ' 返回上一级目录')
    list2.itemconfig(0, fg='green')
    for i in range(len(data)):
        list2.insert(tkinter.END, (' '+data[i]))
        if not '.' in data[i]:
            list2.itemconfig(tkinter.END, fg='orange')
        else:
            list2.itemconfig(tkinter.END, fg='blue')

# 打印服务端当前工作目录(pwd)
def pwd(enter):
    s.send(enter.encode())
    data = s.recv(1024)
    recvList('dir')
    return data.decode()  # 返回接收到的路径

# 创建标签显示服务端工作目录
def lab():
    global label
    try:
        lu = pwd('pwd')
        label.destroy()
        label = tkinter.Label(ftp, text=lu)
        label.place(x=5, y=0, )
    except:
        lu = pwd('pwd')
        label = tkinter.Label(ftp, text=lu)
        label.place(x=5, y=0, )
lab()

# 进入指定目录(cd)
def cd(message):
    s.send(message.encode())

# 接收下载文件(get)
def get(message):
    name = message.split()
    name = name[1]  # 获取命令的第二个参数(文件名)
    # 选择对话框, 选择文件的保存路径
    fileName = tkinter.filedialog.asksaveasfilename(title='保存文件到',
                                        initialfile=name)
    # 如果文件名非空才进行下载
    if fileName:
        print('开始下载文件!')
        s.send(message.encode())
        with open(fileName, 'wb') as f:
            while True:
                data = s.recv(1024)
                if data == 'EOF'.encode():
                    print('下载完成!')
                    break
                f.write(data)

# 创建用于绑定在列表框上的函数
def run(*args):
    indexs = list2.curselection()
    index = indexs[0]
    content = list2.get(index)
    print(content)
    # 如果有一个.则为文件
    if '.' in content:
        content = 'get' + content
        get(content)
    elif content == ' 返回上一级目录':
        content = 'cd ..'
        cd(content)
    else:
        content = 'cd ' + content
        cd(content)
    lab()  # 刷新显示页面
    
# 在列表框上设置绑定事件
list2.bind('<ButtonRelease-1>', run)

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
#main()
