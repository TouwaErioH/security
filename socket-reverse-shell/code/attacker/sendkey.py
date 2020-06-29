import socket
import os
import random
import rsa
import time

#with open('/home/erio/Desktop/attacker/attpublic.pem') as publickfile: #自动 close
with open('/home/erio/Desktop/attacker/attpublic.pem') as publickfile: #自动 close
    p = publickfile.read()
    mypub=rsa.PublicKey.load_pkcs1(p)

with open('/home/erio/Desktop/attacker/attprivate.pem') as privatefile: #自动 close
    p = privatefile.read()
    mypri=rsa.PrivateKey.load_pkcs1(p)

with open('/home/erio/Desktop/attacker/daepublic.pem') as publickfile: #自动 close
    p = publickfile.read()
    otherpub=rsa.PublicKey.load_pkcs1(p)

N1=random.randint(1234,9999)	#确定长度的随机数，这样方便分开
N1=str(N1)
IDAttack='IDAttacker' #ID


client = socket.socket()  # 生成socket连接对象
ip_port =("localhost", 43333)  # 地址和端口号
client.connect(ip_port)  # 连接
print("服务器已连接")

for i in range(1):
    msg=N1+IDAttack
    msg=msg.encode('utf-8')
    crypto = rsa.encrypt(msg,otherpub) #crypto bytes类型
    client.send(crypto)  # 传送和接收都是bytes类型
    print("step 1 succeed\n")

    data = client.recv(1024)  # 接收
    content = rsa.decrypt(data, mypri) #解密后还是bytes （bytes相当于str.encode(utf-8)）
    N11=content[0:4]
    N2=content[4:]
    if N11!=N1.encode('utf-8'):
        print("N11!=N1\n")
        exit(1)
    print("step 2 succeed\n")

    msg=N2
    crypto = rsa.encrypt(msg,otherpub)
    time.sleep(0.1)
    client.send(crypto)  # 传送和接收都是bytes类型
    print("step 3 succeed\n")

    key="keyskeyskeyskeys"  #128 bit
    with open('/home/erio/Desktop/attacker/key.txt','r') as aesfile: #自动 close
        key = aesfile.read()
        print(len(key))  #str
    key=key[0:16]   #/R/N 之类的影响
    msg=key.encode('utf-8')
    mysign = rsa.sign(msg, mypri, 'SHA-1') #签名
    msg=msg+mysign
    crypto = rsa.encrypt(msg,otherpub)
    time.sleep(0.1)
    client.send(crypto)  # 传送和接收都是bytes类型   
    print("step 4 succeed\n")
client.close()
