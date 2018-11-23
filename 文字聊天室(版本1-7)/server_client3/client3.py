'''
    创建图形界面, 将打印和发送(回车)都加到图形界面中
    因为将发送功能加入了图形界面, 所以将同样是发送部分的main函数删掉
'''

import socket
import threading
import json
import tkinter

IP = '127.0.0.1'
PORT = 50007
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect( (IP, PORT) )

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
