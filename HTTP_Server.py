from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM) # IPv4, TCP 방식
serverSocket.bind(('', 8080)) # 소켓과 AF를 연결 (IP, PORT)
serverSocket.listen(1) # 1개의 접속 허용

connectionSocket, addr = serverSocket.accept() # 접속 대기 후 수락

print(str(addr), '에서 접속이 확인되었습니다.')