from socket import *
from socket import timeout

serverName = 'localhost'
serverPort = 8080

def recv_all(sock):
    sock.settimeout(1)
    data = b""
    try:
        while True:
            part = sock.recv(4096)
            if not part:
                break
            data += part
    except timeout:
        pass
    return data.decode()

def send_request(request_bytes, send_body=None):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(request_bytes)
        response = recv_all(clientSocket)

        if send_body and "100 Continue" in response:
            clientSocket.send(send_body)
            response += "\n" + recv_all(clientSocket)

        clientSocket.close()
        return response
    except Exception as e:
        return f"[ERROR] {e}"

def CASE1():
    print("======= CASE1 - GET 200 OK =======")
    request = (
        "GET / HTTP/1.1\r\n"
        f"Host: {serverName}:{serverPort}\r\n"
        "User-Agent: Custom/1.0\r\n"
        "Connection: close\r\n\r\n"
    )
    response = send_request(request.encode())
    print(response)
    return request, response

def CASE2():
    print("======= CASE2 - GET 404 Not Found =======")
    request = (
        "GET /NotFoundError HTTP/1.1\r\n"
        f"Host: {serverName}:{serverPort}\r\n"
        "User-Agent: Custom/1.0\r\n"
        "Connection: close\r\n\r\n"
    )
    response = send_request(request.encode())
    print(response)
    return request, response

def CASE3():
    print("======= CASE3 - POST 100 Continue + 200 OK =======")
    message = "Hello World"
    request = (
        "POST / HTTP/1.1\r\n"
        f"Host: {serverName}:{serverPort}\r\n"
        "Expect: 100-Continue\r\n"
        "User-Agent: Custom/1.0\r\n"
        f"Content-Length: {len(message)}\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n\r\n"
    )
    response = send_request(request.encode(), (message + "\r\n").encode())
    print(response)
    return request, response

def CASE4():
    print("======= CASE4 - POST 400 Bad Request (empty string) =======")
    message = " "
    request = (
        "POST / HTTP/1.1\r\n"
        f"Host: {serverName}:{serverPort}\r\n"
        "Expect: 100-Continue\r\n"
        "User-Agent: Custom/1.0\r\n"
        f"Content-Length: {len(message)}\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n\r\n"
    )
    response = send_request(request.encode(), (message + "\r\n").encode())
    print(response)
    return request, response

def CASE5():
    print("======= CASE5 - POST 404 Not Found =======")
    message = "hello world"
    request = (
        "POST /NotFoundError HTTP/1.1\r\n"
        f"Host: {serverName}:{serverPort}\r\n"
        "Expect: 100-Continue\r\n"
        "User-Agent: Custom/1.0\r\n"
        f"Content-Length: {len(message)}\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n\r\n"
    )
    response = send_request(request.encode(), (message + "\r\n").encode())
    print(response)
    return request, response

def CASE6():
    print("======= CASE6 - HEAD 200 OK =======")
    request = (
        "HEAD / HTTP/1.1\r\n"
        f"Host: {serverName}:{serverPort}\r\n"
        "User-Agent: Custom/1.0\r\n"
        "Connection: close\r\n\r\n"
    )
    response = send_request(request.encode())
    print(response)
    return request, response

def CASE7():
    print("======= CASE7 - HEAD 404 Not Found =======")
    request = (
        "HEAD /NotFoundError HTTP/1.1\r\n"
        f"Host: {serverName}:{serverPort}\r\n"
        "User-Agent: Custom/1.0\r\n"
        "Connection: close\r\n\r\n"
    )
    response = send_request(request.encode())
    print(response)
    return request, response

def CASE8():
    print("======= CASE8 - PUT 200 OK =======")
    filename = "test.jpeg"
    content_type = "image/jpeg"
    with open(filename, "rb") as file:
        file_content = file.read()

    request = (
        f"PUT /{filename} HTTP/1.1\r\n"
        f"Host: {serverName}:{serverPort}\r\n"
        f"Expect: 100-Continue\r\n"
        f"User-Agent: Custom/1.0\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(file_content)}\r\n"
        f"Connection: close\r\n\r\n"
    )
    response = send_request(request.encode(), file_content)
    print(response)
    return request, response

def CASE9():
    print("======= CASE9 - PUT 400 Bad Request (too large) =======")
    filename = "400_Bad_Request.png"
    content_type = "image/png"
    with open(filename, "rb") as file:
        file_content = file.read()

    request = (
        f"PUT /{filename} HTTP/1.1\r\n"
        f"Host: {serverName}:{serverPort}\r\n"
        f"Expect: 100-Continue\r\n"
        f"User-Agent: Custom/1.0\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(file_content)}\r\n"
        f"Connection: close\r\n\r\n"
    )
    response = send_request(request.encode(), file_content)
    print(response)
    return request, response

if __name__ == "__main__":
    CASE1()
    CASE2()
    CASE3()
    CASE4()
    CASE5()
    CASE6()
    CASE7()
    CASE8()
    CASE9()