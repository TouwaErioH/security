import socket
import os
import hashlib
import time
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


# 解密后，去掉补足的空格用strip() 去掉. 返回的是str
def decrypt(text,key):
    key = key.encode('utf-8')
    mode = AES.MODE_ECB
    cryptor = AES.new(key, mode)
    plain_text = cryptor.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')

with open('/home/erio/Desktop/attacker/key.txt','r') as aesfile: #自动 close
        aeskey = aesfile.read()
        aeskey=aeskey[0:16]
print('aes EBC key:%s \n'%(aeskey))

print("新一轮接收开始\n")
client = socket.socket()  # 生成socket连接对象
ip_port =("localhost", 43232)  # 地址和端口号
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
        file_name = server_response
        file_name=decrypt(file_name,aeskey)

        print("文件名：", file_name)
        client.send(msg.encode("utf-8")) #发送确认
		
        # 1.先接收长度，建议8192
        server_response = client.recv(1024)
        file_size=decrypt(server_response,aeskey)
        file_size = int(file_size)
        print("接收到的字节大小：", file_size)
        client.send(msg.encode("utf-8")) #发送确认	
		
        # 2.接收文件内容
        client.send("准备好接收".encode("utf-8"))  # 接收确认
        nowtime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        filename = file_name[:-4] +nowtime+'.txt' 
        f = open(filename, "w")  # wb是字节写入
        received_size = 0
        m = hashlib.md5()

        while received_size < file_size:  #每次读一行写入 
            data = client.recv(1024)  # 多次接收内容，接收大数据; 发送方设置延迟0.1s，来防止粘包
            data=decrypt(data,aeskey)   # 这里decrypt 得到的str 包含 b' xxxxx '。下面去掉b' '，得到形如 'whu\n' 的str。 
            #print(data)
            #data=data[2:-1]   #去掉 b','
            #print(data)
            #print('\n')
            dataenc=data.encode('utf-8')  #保持一致
            #print(dataenc)
            #print('\n')
            data_len = len(data) #去掉最后的\r\n占的长度
            received_size += data_len
            print("已接收：", int(received_size/file_size*100), "%")
            m.update(dataenc)
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
