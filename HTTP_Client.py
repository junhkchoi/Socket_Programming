from socket import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('121.0.0.1', 8080)) # 클라이언트에서 서버로 접속 (자신의 IP, PORT)

print('연결 확인됐습니다.')
clientSocket.send('I am a client'.encode('utf-8'))

print('클라이언트가 메세지를 전송했습니다')

data = clientSocket.recv(1024)
print('받은 데이터: ', data.decode('utf-8'))