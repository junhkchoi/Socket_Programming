from socket import *

serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Server started at Port:', serverPort)

def request_parser(message):
    try:
        lines = message.split("\r\n")
        request_line = lines[0].split()
        method = request_line[0]
        path = request_line[1]
        print("Method:", method)
        print("Path:", path)
        print()
        return lines, request_line, method, path
    except Exception as e:
        print("Error:", e)
        return None, None, None, None

def another_request(connectionSocket):
    body = "<html><body><h1>405 Method Not Allowed</h1></body></html>"
    response = (
        "HTTP/1.1 405 Method Not Allowed\r\n"
        f"Content-Type: text/html\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n"
        f"{body}"
    )
    connectionSocket.send(response.encode())

def GET(connectionSocket, path):
    if path == "/":
        body = "<html><script>alert('Hello!');</script></html>"
        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/html\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n"
            f"{body}"
        )
    else:
        body = "<html><body><h1>404 Not Found</h1></body></html>"
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            f"Content-Type: text/html\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n"
            f"{body}"
        )
    connectionSocket.send(response.encode())

def POST(connectionSocket, message, path):
    if "Expect: 100-Continue" in message and path == "/":
        connectionSocket.send("HTTP/1.1 100 Continue\r\n\r\n".encode())
        body = connectionSocket.recv(1024).decode().strip().upper()

        if 0 < len(body) <= 30:
            response_body = f"<html><body><h1>{body}</h1></body></html>"
            response = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/html\r\nContent-Length: {len(response_body)}\r\nConnection: close\r\n\r\n"
                f"{response_body}"
            )
        else:
            response_body = "<html><body><h1>400 Bad Request</h1></body></html>"
            response = (
                "HTTP/1.1 400 Bad Request\r\n"
                f"Content-Type: text/html\r\nContent-Length: {len(response_body)}\r\nConnection: close\r\n\r\n"
                f"{response_body}"
            )
    else:
        response_body = "<html><body><h1>404 Not Found</h1></body></html>"
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            f"Content-Type: text/html\r\nContent-Length: {len(response_body)}\r\nConnection: close\r\n\r\n"
            f"{response_body}"
        )
    connectionSocket.send(response.encode())

def HEAD(connectionSocket, path):
    if path == "/":
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        )
    else:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        )
    connectionSocket.send(response.encode())

def PUT(connectionSocket, message, path):
    content_length = None
    for header in message.split("\r\n"):
        if header.startswith("Content-Length:"):
            content_length = int(header.split(":")[1].strip())
            break

    max_size = 8192
    if content_length is None or content_length > max_size:
        body = "<html><body><h1>400 Bad Request</h1></body></html>"
        response = (
            "HTTP/1.1 400 Bad Request\r\n"
            f"Content-Type: text/html\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n"
            f"{body}"
        )
        connectionSocket.send(response.encode())
        return

    if "Expect: 100-Continue" in message:
        connectionSocket.send("HTTP/1.1 100 Continue\r\n\r\n".encode())
        body = connectionSocket.recv(content_length)

        if len(body) <= max_size:
            filename = path.strip("/")
            with open(filename, "wb") as f:
                f.write(body)

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
            )
            connectionSocket.send(response.encode())

while True:
    connectionSocket, addr = serverSocket.accept()
    print("Connection from", addr)

    try:
        message = connectionSocket.recv(1024).decode()
        print("Received request")
        print(message)

        lines, request_line, method, path = request_parser(message)
        if method is None:
            continue

        if method == "GET":
            GET(connectionSocket, path)
        elif method == "HEAD":
            HEAD(connectionSocket, path)
        elif method == "POST":
            POST(connectionSocket, message, path)
        elif method == "PUT":
            PUT(connectionSocket, message, path)
        else:
            another_request(connectionSocket)

    except Exception as e:
        print("Error:", e)
        body = "<html><body><h1>500 Internal Server Error</h1></body></html>"
        response = (
            "HTTP/1.1 500 Internal Server Error\r\n"
            f"Content-Type: text/html\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n"
            f"{body}"
        )
        connectionSocket.send(response.encode())

    connectionSocket.close()