#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cerrno>
#include <cstring>

#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include<vector>

void reverse(int s1,char * reply){
  for(int i=0,j=strlen(reply)-1;i<j;i++,j--){
        char c=reply[i];
		reply[i]=reply[j];
        reply[j]=c;
  }
  send (s1, reply, strlen(reply),0);
}

int process_request (int s1, char *reply)

{
  char result[256];  //exploit address= &result+16  (rbp+rip)
  strcpy (result, reply);
  send(s1, result, strlen(result),0);
  printf ("Result: %p\n", &result);
  return 0;
}


int main() {
    std::cout << "server on" << std::endl;
    // socket
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);  //listenfd 服务器socket描述字
    if (listenfd == -1) {
        std::cout << "Error: socket" << std::endl;
        return 0;
    }
    // bind
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(12345);
    //addr.sin_addr.s_addr = INADDR_ANY; //INADDR-ANY local
    addr.sin_addr.s_addr=inet_addr("127.0.0.1");   
    if (bind(listenfd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
        std::cout << "Error: bind" << std::endl;
        return 0;
    }
    // listen
    if(listen(listenfd, 5) == -1) {
        std::cout << "Error: listen" << std::endl;
        return 0;
    }
    // accept
    int conn;
    char clientIP[INET_ADDRSTRLEN] = "";
    struct sockaddr_in clientAddr;
    socklen_t clientAddrLen = sizeof(clientAddr);
    while (true) {
        std::cout << "...listening" << std::endl;
        conn = accept(listenfd, (struct sockaddr*)&clientAddr, &clientAddrLen);
        if (conn < 0) {
            std::cout << "Error: accept" << std::endl;
            continue;
        }
        inet_ntop(AF_INET, &clientAddr.sin_addr, clientIP, INET_ADDRSTRLEN);//二进制转化为点分十进制
        std::cout << "...connect " << clientIP << ":" << ntohs(clientAddr.sin_port) << std::endl;

        char buf[332];  // 容量
        while (true) {
            memset(buf, 0, sizeof(buf));
			extern int errno;  //错误标志
            int len = recv(conn, buf, sizeof(buf), 0);//recv 而不是write，不会一直等待
            buf[len] = '\0';
            if (strcmp(buf, "quit") == 0) {
                std::cout << "...disconnect " << clientIP << ":" << ntohs(clientAddr.sin_port) << std::endl;
                break;
            }
			
			if(len<=0){
			 if(errno != EINTR)
                std::cout << "...disconnect " << clientIP << ":" << ntohs(clientAddr.sin_port) << std::endl;
                break;
			}
			
            printf("received %s\n",buf);

            process_request(conn,buf);
	reverse(conn,buf);

        }
        
        close(conn);
    }
    close(listenfd);
    return 0;
}
