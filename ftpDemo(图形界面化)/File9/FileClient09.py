'''
    将在控制台打印的下载和上传成功信息改用弹出对话框
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
def recvList(enter, lu):
    s.send(enter.encode())
    data = s.recv(4096)  
    data = json.loads(data.decode())
    list2.delete(0, tkinter.END)  # 清空列表框
    lu = lu.split('\\')
    if len(lu) != 1:
        list2.insert(tkinter.END, ' 返回上一级目录')
        list2.itemconfig(0, fg='green')
    for i in range(len(data)):
        list2.insert(tkinter.END, (' '+data[i]))
        if not '.' in data[i]:
            list2.itemconfig(tkinter.END, fg='orange')
        else:
            list2.itemconfig(tkinter.END, fg='blue')

# 创建标签显示服务端工作目录
def lab():
    global label
    data = s.recv(1024)  # 接收目录
    lu = data.decode()
    try:
        label.destroy()
        label = tkinter.Label(ftp, text=lu)
        label.place(x=5, y=0, )
    except:
        label = tkinter.Label(ftp, text=lu)
        label.place(x=5, y=0, )
    recvList('dir', lu)

# 进入指定目录(cd)
def cd(message):
    s.send(message.encode())

# 刚连接上服务端时进行一次面板刷新    
cd('cd same')
lab()

# 接收下载文件(get)
def get(message):
    name = message.split()
    name = name[1]  # 获取命令的第二个参数(文件名)
    # 选择对话框, 选择文件的保存路径
    fileName = tkinter.filedialog.asksaveasfilename(title='保存文件到',
                                        initialfile=name)
    # 如果文件名非空才进行下载
    if fileName:
        s.send(message.encode())
        with open(fileName, 'wb') as f:
            while True:
                data = s.recv(1024)
                if data == 'EOF'.encode():
                    tkinter.messagebox.showinfo(title='提示',
                                                message='下载成功!')
                    break
                f.write(data)

# 创建用于绑定在列表框上的函数
def run(*args):
    indexs = list2.curselection()
    index = indexs[0]
    content = list2.get(index)
    # 如果有一个 . 则为文件
    if '.' in content:
        content = 'get' + content
        get(content)
        cd('cd same')
    elif content == ' 返回上一级目录':
        content = 'cd ..'
        cd(content)
    else:
        content = 'cd ' + content
        cd(content)
    lab()  # 刷新显示页面
    
# 在列表框上设置绑定事件
list2.bind('<ButtonRelease-1>', run)

# 上传客户端所在文件夹中指定的文件到服务端, 在函数中获取文件名, 不用传参数
def put():
    # 选择对话框
    fileName = tkinter.filedialog.askopenfilename(title='选择上传文件')
    # 如果有选择文件才继续执行
    if fileName:
        name = fileName.split('/')[-1]
        message = 'put ' + name
        s.send(message.encode())
        with open(fileName, 'rb') as f:
            while True:
                a = f.read(1024)
                if not a:
                    break
                s.send(a)
            time.sleep(0.1)  # 延时确保文件发送完整
            s.send('EOF'.encode())
            tkinter.messagebox.showinfo(title='提示',
                                        message='上传成功!')
    cd('cd same')
    lab()  # 上传成功后刷新显示页面

# 创建上传按钮, 并绑定上传文件功能
upload = tkinter.Button(ftp, text='上传文件', command=put)
upload.place(x=5, y=360, height=30, width=70)

# 关闭文件管理器, 待完善
def closeFile():
    global mark
    mark = 0;
    s.send('quit'.encode())
    s.close()
    ftp.destroy()

# 创建关闭按钮
close = tkinter.Button(ftp, text='关闭', command=closeFile)
close.place(x=80, y=360, height=30, width=70)

ftp.mainloop()
