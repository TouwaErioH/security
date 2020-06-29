import socket
import os
import hashlib
import time

print("新一轮接收开始\n")
client = socket.socket()  # 生成socket连接对象
ip_port =("localhost", 23232)  # 地址和端口号
client.connect(ip_port)  # 连接
print("服务器已连接")
msg='read to recv'
client.send(msg.encode("utf-8"))  # 传送和接收都是bytes类型
try:
    while True:
        # 0. 接受文件名
        server_response = client.recv(1024)
#        if not server_response:  # 可能跳过了一次文件发送
#                continue
        file_name = server_response.decode("utf-8")
        print("文件名：", file_name)
        client.send(msg.encode("utf-8")) #发送确认		
        # 1.先接收长度，建议8192
        server_response = client.recv(1024)
        file_size = int(server_response.decode("utf-8"))
        print("接收到的大小：", file_size)
        client.send(msg.encode("utf-8")) #发送确认	
        # 2.接收文件内容
        client.send("准备好接收".encode("utf-8"))  # 接收确认
        nowtime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        filename = file_name[:-4] +nowtime+'.txt' 
        f = open(filename, "wb")
        received_size = 0
        m = hashlib.md5()

        while received_size < file_size:
            size = 0  # 准确接收数据大小，解决粘包
            if file_size - received_size > 1024: # 多次接收
                size = 1024
            else:  # 最后一次接收完毕
                size = file_size - received_size

            data = client.recv(size)  # 多次接收内容，接收大数据
            data_len = len(data)
            received_size += data_len
            print("已接收：", int(received_size/file_size*100), "%")

            m.update(data)
            f.write(data)

        f.close()

        print("实际接收的大小:", received_size)  # 解码

        # 3.md5值校验
        md5_sever = client.recv(1024).decode("utf-8")
        md5_client = m.hexdigest()
        client.send(msg.encode("utf-8")) #发送确认	
        print("服务器发来的md5:", md5_sever)
        print("接收文件的md5:", md5_client)
        if md5_sever == md5_client:
            print("MD5值校验成功")
        else:
            print("MD5值校验失败")
except:
    print("当前轮接受结束，daemon进入下一次探测阶段;5S后可再次连接获取文件\n")