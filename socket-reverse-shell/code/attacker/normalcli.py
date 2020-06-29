
# 扫描端口 python

import socket
import os
import subprocess
print("客户端开启")
# 创建套接字
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345

try:
    mySocket.connect((host, port))  ##连接到服务器
    print("连接到服务器")
except:  ##连接不成功，运行最初的ip
    print('连接不成功')

while True:
    # 发送消息
    msg = input("客户端发送:")
    if msg == "attack":
        print("wait until this process exit and use attack.pl to get remote shell!!")
        msg="quit"
        mySocket.send(msg.encode(encoding='utf-8'))
        mySocket.close()
        print("程序结束\n")
        exit()
        #这样不可行，因为排队的缘故python连接不结束perl的连接不能执行
		#subprocess.call(["perl", "/home/erio/Desktop/attack.pl"])
        #os.system("pause")

    mySocket.send(msg.encode(encoding='utf-8'))
    print("发送完成")
    if msg == "quit":
        mySocket.close()
        print("程序结束\n")
        exit()
    # 接收消息
    msg = mySocket.recv(len(msg))
    print("客户端接收,origin：%s" % msg.decode("utf-8"))  # 把接收到的数据进行解码
    msg = mySocket.recv(len(msg))
    print("客户端接收,reversed：%s" % msg.decode("utf-8"))  # 把接收到的数据进行解码
    print("读取完成")
print("程序结束\n")

