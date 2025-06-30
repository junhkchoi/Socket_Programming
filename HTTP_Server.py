from socket import *

SERVER_PORT = 8080

serverSock = socket(AF_INET, SOCK_STREAM) # 1. 서버 소켓 생성 (IPv4, TCP)
serverSock.bind(('', SERVER_PORT)) # 2. 빈 문자열 ''은 모든 IP에서 접속을 허용, 8080번 포트로 바인딩
serverSock.listen(1) # 3. 연결 대기 (최대 1개까지 연결 대기)

print(f"{SERVER_PORT}번 포트로 접속 대기 중...")

connectionSock, addr = serverSock.accept() # 4. 클라이언트 연결 수락
print(str(addr), '에서 접속이 확인되었습니다.')

# 5. 클라이언트가 보낸 데이터 수신 (1024바이트까지)

while (True):
    sendData = input('>>>')
    connectionSock.send(sendData.encode('utf-8'))
    
    recvData = connectionSock.recv(1024)
    print('상대방 :', recvData.decode('utf-8'))