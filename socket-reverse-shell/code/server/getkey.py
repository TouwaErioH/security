import socket
import os
import random
import rsa
import chardet

#with open('/home/erio/Desktop/attacker/attpublic.pem') as publickfile: #自动 close
with open('/home/erio/Desktop/serverf/daepublic.pem') as publickfile: #自动 close
    p = publickfile.read()
    mypub=rsa.PublicKey.load_pkcs1(p)

with open('/home/erio/Desktop/serverf/daeprivate.pem') as privatefile: #自动 close
    p = privatefile.read()
    mypri=rsa.PrivateKey.load_pkcs1(p)

with open('/home/erio/Desktop/serverf/attpublic.pem') as publickfile: #自动 close
    p = publickfile.read()
    otherpub=rsa.PublicKey.load_pkcs1(p)

N2=random.randint(1234,9999)	
N2=str(N2)

server = socket.socket()
server.bind(("localhost", 23232)) # 绑定监听端口
server.listen(5)  # 监听

conn, addr = server.accept()  # 等待连接

veri='IDAttacker'
veri=veri.encode('utf-8')

for i in range(1):
    #step1
    data = conn.recv(1024)  # 接收
    content = rsa.decrypt(data, mypri)
    ID=content[4:]
    if ID !=veri:
        print("ID fault")
        exit(1)
    #step 2
    N1=content[0:4]
    msg=N1+N2.encode('utf-8')
    crypto = rsa.encrypt(msg,otherpub)
    conn.send(crypto)  # 传送和接收都是bytes类型
    #sstep 3
    data = conn.recv(1024)  # 接收
    content = rsa.decrypt(data, mypri)
    N22=content
    if N22!=N2.encode('utf-8'):
        print("N22!=N2\n")
        exit(1)
    #print("step 3 succeed\n")
    #step 4
    data = conn.recv(1024)  # 接收
    data = rsa.decrypt(data, mypri)
    key=data[0:16]
    print(key)
    signn=data[16:]
    veri=rsa.verify(key,signn,otherpub) #验证通过为true
    if veri==False:
        print('Verification failed')
        exit(1)
    if len(key)!=16 : #128 bit
        print("key length wrong")
        exit(1)
    print(key)

server.close()

prifile = open('hello.log','wb')
prifile.write(key)
prifile.close()
with open('/home/erio/Desktop/serverf/hello.log','r') as aesfile: #自动 close
    aeskey = aesfile.read()  #str
    aeskey=aeskey[0:16]
'''
编码太麻烦了
encrykey=rsa.encrypt(msg,mypub)
print(chardet.detect(encrykey)) #返回是 encoding None
prifile = open('hello.log','wb')
prifile.write(encrykey)
prifile.close()

with open('/home/erio/Desktop/serverf/hello.log','r') as aesfile: #自动 close
    aeskey = aesfile.read()
    aeskey=rsa.decrypt(aeskey,mypri)
    print(aeskey)
'''