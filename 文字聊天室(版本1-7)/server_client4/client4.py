'''
    创建登录界面(还没有功能)
'''

import socket
import threading
import json
import tkinter

IP = ''
PORT = ''
user = ''

## 登录窗口
root1 = tkinter.Tk()
root1.title('登录')
root1['height'] = 110
root1['width'] = 250

IP1 = tkinter.StringVar()
IP1.set('127.0.0.1:50007')
User = tkinter.StringVar()
User.set('')

# 服务器标签
labelIP = tkinter.Label(root1, text='服务器地址')
labelIP.place(x=20, y=10, width=80, height=20)

entryIP = tkinter.Entry(root1, width=80, textvariable=IP1)
entryIP.place(x=110, y=10, width=110, height=20)

# 用户名标签
labelUser = tkinter.Label(root1, text='用户名')
labelUser.place(x=20, y=40, width=80, height=20)

entryUser = tkinter.Entry(root1, width=80, textvariable=User)
entryUser.place(x=110, y=40, width=110, height=20)

# 登录按钮
def login(event=0):
    global IP, PORT, user
    IP, PORT = entryIP.get().split(':')  # 获取IP和端口号
    PORT = int(PORT)  # 端口号需要为int类型
    user = entryUser.get()
    root1.destroy()  # 关闭窗口
root1.bind('<Return>', login)

but = tkinter.Button(root1, text='登录', command=login)
but.place(x=90, y=70, width=70, height=30)

root1.mainloop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
if user:
    s.send(user.encode())
else:
    s.send('no'.encode())  # 没有输入用户名则标记


## 聊天窗口
# 创建图形界面
root = tkinter.Tk()
root.title('text')
root['height'] = 330
root['width'] = 450

# 创建多行文本框
listbox = tkinter.Listbox(root, width=300)
listbox.place(x=5, y=0, width=440, height=280)

# 创建输入文本框和关联变量
a = tkinter.StringVar()
a.set('')
entry = tkinter.Entry(root, width=120, textvariable=a)
entry.place(x=5, y=285, width=300, height=30)

def send(event=0):
    mes = entry.get()
    s.send(mes.encode())
    a.set('')  # 发送后清空文本框
# 创建发送按钮
button = tkinter.Button(root, text='发送', command=send)
button.place(x=310, y=285, width=60, height=30)
root.bind('<Return>', send)  # 绑定回车发送信息

# 用于时刻接收服务端发送的信息并打印
def recv():
    while True:
        data = s.recv(1024)
        data = json.loads(data.decode())
        print(data)
        listbox.insert(tkinter.END, data)  # END将信息加在最后一行
        
r = threading.Thread(target=recv)
r.start()

root.mainloop()
s.close()  # 关闭图形界面后关闭TCP连接
input()  # 方便查看错误

