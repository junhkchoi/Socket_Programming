from socket import *

serverName = 'localhost'
serverPort = 8080

def CASE1():  # GET / → 200 OK
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    request = f"GET / HTTP/1.1\r\nHost: {serverName}:{serverPort}\r\nUser-Agent: Custom/1.0\r\nConnection: close\r\n\r\n"
    clientSocket.send(request.encode())
    response = clientSocket.recv(4096).decode()
    clientSocket.close()
    return request, response

def CASE2():  # GET /NotFound → 404 Not Found
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    request = f"GET /NotFound HTTP/1.1\r\nHost: {serverName}:{serverPort}\r\nUser-Agent: Custom/1.0\r\nConnection: close\r\n\r\n"
    clientSocket.send(request.encode())
    response = clientSocket.recv(4096).decode()
    clientSocket.close()
    return request, response

def CASE3():  # POST / Expect: 100-Continue with body → 100 Continue → 200 OK
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    message = "Hello World"
    request = (f"POST / HTTP/1.1\r\nHost: {serverName}:{serverPort}\r\nExpect: 100-Continue\r\n"
               f"User-Agent: Custom/1.0\r\nContent-Length: {len(message)}\r\nContent-Type: text/plain\r\n\r\n")
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024).decode()
    if "100 Continue" in response:
        clientSocket.send((message + "\r\n").encode())
        response += "\n" + clientSocket.recv(1024).decode()
    clientSocket.close()
    return request + message, response

def CASE4():  # POST / Expect: 100-Continue with empty body → 100 Continue → 400 Bad Request
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    message = ""
    request = (f"POST / HTTP/1.1\r\nHost: {serverName}:{serverPort}\r\nExpect: 100-Continue\r\n"
               f"User-Agent: Custom/1.0\r\nContent-Length: {len(message)}\r\nContent-Type: text/plain\r\n\r\n")
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024).decode()
    if "100 Continue" in response:
        clientSocket.send((message + "\r\n").encode())
        response += "\n" + clientSocket.recv(1024).decode()
    clientSocket.close()
    return request + message, response

def CASE5():  # POST /no_such_path → 404 Not Found
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    message = "hello world"
    request = (f"POST /no_such_path HTTP/1.1\r\nHost: {serverName}:{serverPort}\r\nExpect: 100-Continue\r\n"
               f"User-Agent: Custom/1.0\r\nContent-Length: {len(message)}\r\nContent-Type: text/plain\r\n\r\n" + message)
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024).decode()
    clientSocket.close()
    return request, response

def CASE6():  # PUT /file.txt with small body → 100 Continue → 200 OK
    filename = "test.jpeg"
    content_type = "image/jpeg"
    with open(filename, "rb") as file:
        file_content = file.read()
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    request = (f"PUT /{filename} HTTP/1.1\r\nHost: {serverName}:{serverPort}\r\nExpect: 100-Continue\r\n"
               f"User-Agent: Custom/1.0\r\nContent-Length: {len(file_content)}\r\nContent-Type: {content_type}\r\n\r\n")
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024).decode()
    if "100 Continue" in response:
        clientSocket.send(file_content)
        response += "\n" + clientSocket.recv(1024).decode()
    clientSocket.close()
    return request, response

def CASE7():  # PUT /bigfile.bin → 400 Bad Request
    filename = "400_Bad_Request.png"
    content_type = "image/png"
    with open(filename, "rb") as file:
        file_content = file.read()
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    request = (f"PUT /{filename} HTTP/1.1\r\nHost: {serverName}:{serverPort}\r\nExpect: 100-Continue\r\n"
               f"User-Agent: Custom/1.0\r\nContent-Length: {len(file_content)}\r\nContent-Type: {content_type}\r\n\r\n")
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024).decode()
    clientSocket.close()
    return request, response

def CASE8():  # HEAD / → 200 OK
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    request = f"HEAD / HTTP/1.1\r\nHost: {serverName}:{serverPort}\r\nUser-Agent: Custom/1.0\r\nConnection: close\r\n\r\n"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024).decode()
    clientSocket.close()
    return request, response

def CASE9():  # HEAD /missing → 404 Not Found
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    request = f"HEAD /missing HTTP/1.1\r\nHost: {serverName}:{serverPort}\r\nUser-Agent: Custom/1.0\r\nConnection: close\r\n\r\n"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024).decode()
    clientSocket.close()
    return request, response


if __name__ == "__main__":
    for i in range(1, 9):
        req, res = globals()[f"CASE{i}"]()
        print(f"\n=== CASE{i} ===\nRequest:\n{req}\nResponse:\n{res}\n")