from socket import *

# 1. 클라이언트 소켓 생성 (IPv4, TCP)
clientSock = socket(AF_INET, SOCK_STREAM)

# 2. 서버에 연결 요청
clientSock.connect(('127.0.0.1', 8080))  # 또는 'localhost'
print('연결 확인 됐습니다.')

# 3. 서버에 메시지 전송
clientSock.send('I am a client'.encode('utf-8'))
print('메시지를 전송했습니다.')

# 4. 서버로부터 메시지 수신
data = clientSock.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))