from socket import *

SERVER_PORT = 8080

# 1. 클라이언트 소켓 생성 (IPv4, TCP)
clientSock = socket(AF_INET, SOCK_STREAM)

# 2. 서버에 연결 요청
clientSock.connect(('localhost', SERVER_PORT))  # 또는 'localhost'
print('접속 완료!')

# 3. 서버에 메시지 전송
while (True):
    recvData = clientSock.recv(1024)
    print('상대방 :', recvData.decode('utf-8'))
    sendData = input('>>>')
    clientSock.send(sendData.encode('utf-8'))
