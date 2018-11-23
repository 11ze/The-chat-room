'''
   创建第二个列表框显示在线用户
   将自己发的信息显示成蓝色字体
'''

import socket
import threading
import json  # json.dumps(some)打包   json.loads(some)解包
import tkinter

IP = ''
PORT = ''
user = ''
listbox1 = ''  # 用于显示在线用户的列表框
ii = 0  # 用于判断是开还是关闭列表框

## 登录窗口
root1 = tkinter.Tk()
root1.title('登录')
root1['height'] = 110
root1['width'] = 270

IP1 = tkinter.StringVar()
IP1.set('172.17.148.70:50007')  # 默认显示的ip和端口
User = tkinter.StringVar()
User.set('')

# 服务器标签
labelIP = tkinter.Label(root1, text='服务器地址')
labelIP.place(x=30, y=10, width=80, height=20)

entryIP = tkinter.Entry(root1, width=80, textvariable=IP1)
entryIP.place(x=120, y=10, width=130, height=20)

# 用户名标签
labelUser = tkinter.Label(root1, text='用户名')
labelUser.place(x=30, y=40, width=80, height=20)

entryUser = tkinter.Entry(root1, width=80, textvariable=User)
entryUser.place(x=120, y=40, width=130, height=20)

# 登录按钮
def login(*args):
    global IP, PORT, user
    IP, PORT = entryIP.get().split(':')  # 获取IP和端口号
    PORT = int(PORT)  # 端口号需要为int类型
    user = entryUser.get()
    root1.destroy()  # 关闭窗口
root1.bind('<Return>', login)  # 回车绑定登录功能

but = tkinter.Button(root1, text='登录', command=login)
but.place(x=100, y=70, width=70, height=30)

root1.mainloop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
if user:
    s.send(user.encode())  # 发送用户名
else:
    s.send('no'.encode())  # 没有输入用户名则标记no

# 如果没有用户名则将ip和端口号设置为用户名
addr = s.getsockname()  # 获取客户端ip和端口号
addr = addr[0] + ':' + str(addr[1])
if user == '':
    user = addr

## 聊天窗口
# 创建图形界面
root = tkinter.Tk()
root.title(user)  # 窗口命名为用户名
root['height'] = 330
root['width'] = 450

# 滚动条
#scrolly = tkinter.Scrollbar(root)
#scrolly.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# 创建多行文本框
listbox = tkinter.Listbox(root)  # , yscrollcommand=scrolly.set
listbox.place(x=5, y=0, width=440, height=280)
#scrolly.config(command=listbox.yview)

# 创建输入文本框和关联变量
a = tkinter.StringVar()
a.set('')
entry = tkinter.Entry(root, width=120, textvariable=a)
entry.place(x=5, y=285, width=300, height=30)

def send(*args):
    mes = entry.get()
    s.send(mes.encode())
    a.set('')  # 发送后清空文本框
    
# 创建发送按钮
button = tkinter.Button(root, text='发送', command=send)
button.place(x=310, y=285, width=60, height=30)
root.bind('<Return>', send)  # 绑定回车发送信息

# 创建多行文本框, 现在在线用户
listbox1 = tkinter.Listbox(root)  
listbox1.place(x=315, y=0, width=130, height=280)

def users():
    global listbox1, ii
    if ii == 1:
        listbox1.place(x=315, y=0, width=130, height=280)
        ii = 0
    else:
        listbox1.place_forget()  # 隐藏控件
        ii = 1
    
# 查看在线用户按钮
button1 = tkinter.Button(root, text='在线用户', command=users)
button1.place(x=375, y=285, width=70, height=30)

# 用于时刻接收服务端发送的信息并打印,
def recv():
    while True:
        data = s.recv(1024)
        data = data.decode()
        # 没有捕获到异常则表示接收到的是在线用户列表
        try:
            data = json.loads(data)
            listbox1.delete(0, tkinter.END)  # 清空列表框
            number = ('     在线人数: ' + str(len(data)) + ' 人')
            listbox1.insert(tkinter.END, number)
            listbox1.itemconfig(tkinter.END,fg='green', bg="#f0f0ff") 
            for i in range(len(data)):
                listbox1.insert(tkinter.END, (' '+data[i]))
                listbox1.itemconfig(tkinter.END,fg='green') 
        except:
            listbox.insert(tkinter.END, data)  # END将信息加在最后一行
            listbox.see(tkinter.END)  # 显示在最后
            u = data.split('：')[0]
            if u == ' ' + user:
                listbox.itemconfig(tkinter.END,fg='blue') 
            
        
r = threading.Thread(target=recv)
r.start()  # 开始线程接收信息

root.mainloop()
s.close()  # 关闭图形界面后关闭TCP连接

