  
import socket
import os
import hashlib
import time

def createDaemon():
  import os, sys, time
  #产生子进程，而后父进程退出
  try:
    pid = os.fork()
    if pid > 0:sys.exit(0)
  except OSError as error:
    #print('fork')
    sys.exit(1)
  
  #修改子进程工作目录
  os.chdir("/")
  #创建新的会话，子进程成为会话的首进程
  os.setsid()
  #修改工作目录的umask
  os.umask(0)
  
  #创建孙子进程，而后子进程退出
  try:
    pid = os.fork()
    if pid > 0:
      #print("Daemon PID %d"%pid)
      sys.exit(0)
  except OSError as error:
    #print("fork")
    sys.exit(1)
  run()
  


def search():
    # 搜索文件
    dir = r'/home'  #这里认为home是根目录//可以根据需要自行调整
    specify_str = 'liuqiang'
    spec_type = '.txt'
    # 搜索指定目录
    results = []
    folders = [dir]
    for folder in folders :
        # 把目录下所有文件夹存入待遍历的folders  遍历当前文件夹所有文件名，加到folder，判断是否是文件夹（isdir），是则加入到文件夹列表
        folders += [os.path.join(folder, x) for x in os.listdir(folder) \
                    if os.path.isdir(os.path.join(folder, x))]
        # 把所有满足条件的文件的相对地址存入结果results  是文件（isfile）且含特定字符串
        results += [os.path.relpath(os.path.join(folder, x), start = dir) \
                    for x in os.listdir(folder) \
                    if os.path.isfile(os.path.join(folder, x)) and specify_str in x and spec_type==os.path.join(folder, x)[-4:]]
# 输出结果
    #for result in results:
        #print(result)
    return results

# 可能文件会被修改，所以即使数量不变也重新发送
def senddd(results):
    # 发送文件
    dir = r'/home'#这里认为home是根目录//可以根据需要自行调整
    server = socket.socket()
    server.bind(("localhost", 23232)) # 绑定监听端口
    server.listen(5)  # 监听
    #print("监听开始..")
#    while True:
    conn, addr = server.accept()  # 等待连接
    #print("conn:", conn, "\naddr:", addr)  # conn连接实例
    for i in range(1):
#    while True:
            data = conn.recv(1024)  # 接收
            if not data:  # 客户端已断开
                #print("客户端断开连接")
                break
            for tempfilename in results:
                if True!=os.path.exists(os.path.join(dir,tempfilename )):  #如果在被搜索到而在被发送前就被删除了，打开文件会错误，所以跳过
                    continue
		        # 0. 发送文件名
                filename=os.path.join(dir,tempfilename )
                conn.send(filename.encode("utf-8"))  # 发送文件名
                #print("filename:", filename)
                conn.recv(1024)  # 接收确认				
                # 1.先发送文件大小，让客户端准备接收
                size = os.stat(filename).st_size  #获取文件大小
                conn.send(str(size).encode("utf-8"))  # 发送数据长度
                #print("发送的大小：", size)
                conn.recv(1024)  # 接收确认
                # 2.发送文件内容
                m = hashlib.md5()
                f = open(filename, "rb")
                for line in f:
                    conn.send(line)  # 发送数据
                    m.update(line)
                f.close()
                # 3.发送md5值进行校验
                md5 = m.hexdigest()
                conn.send(md5.encode("utf-8"))  # 发送md5值
                #print("md5:", md5)
                conn.recv(1024)  # 接收确认
                time.sleep(1.0)  #否则接收方可能受到md5+下一个文件的内容/文件名
    server.close()
  
def run():
    while True:
        results=search()
        senddd(results)
        time.sleep(5)
  
if __name__=='__main__':
  createDaemon()