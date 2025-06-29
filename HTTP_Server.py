from socket import *

# 1. 서버 소켓 생성 (IPv4, TCP)
serverSock = socket(AF_INET, SOCK_STREAM)

# 2. 빈 문자열 ''은 모든 IP에서 접속을 허용, 8080번 포트로 바인딩
serverSock.bind(('', 8080))

# 3. 연결 대기 (최대 1개까지 연결 대기)
serverSock.listen(1)

# 4. 클라이언트 연결 수락
connectionSock, addr = serverSock.accept()
print(str(addr), '에서 접속이 확인되었습니다.')

# 5. 클라이언트가 보낸 데이터 수신 (1024바이트까지)
data = connectionSock.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))

# 6. 클라이언트에게 응답 전송
connectionSock.send('I am a server.'.encode('utf-8'))
print('메시지를 보냈습니다.')