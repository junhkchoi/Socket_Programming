from socket import *
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Server started at Port : ', serverPort)

def request_parser(message):
	try:
		# Parse message from client
		# HTTP Structure
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
		response_line = "HTTP/1.1 500 Internal Server Error\r\n"
		headers = "Content-Type: text/html\r\n\r\n"
		body = "<html><head><title></title></head></html>"
		response = response_line + headers
		connectionSocket.send(response.encode())
def another_request():
	response_line = "HTTP/1.1 405 Method Not Allowed\r\n"
	header = "Content-Type: text/html\r\n\r\n"
	body = "<html><head><title></title></head></html>"
	response = response_line + header + body
	connectionSocket.send(response.encode())
	return

def GET(path):
	# CASE1 GET Request 200 OK
	# path : /
	if path == "/":
		# CASE1
		response_line = "HTTP/1.1 200 OK\r\n"
		header = "Content-Type: text/html\r\n\r\n"
		body = "<html><script>alert('Hello!');</script></html>"
		response = response_line + header + body
		connectionSocket.send(response.encode())
	
	# CASE2 - GET Request 404 Not Found Error
	# path : /NotFoundError
	else:
		response_line = "HTTP/1.1 404 Not Found\r\n"
		header = "Content-Type: text/html\r\n\r\n"
		body = "<html><body><h1>404 Not Found</h1></body></html>"
		response = response_line + header + body
		connectionSocket.send(response.encode())
	return

def POST(connectionSocket, message, path):
	# CASE3 PUT Request 100 Continue
	# path: /
	if "Expect: 100-Continue" in message and path == "/":
		response_line = "HTTP/1.1 100 Continue\r\n\r\n"
		connectionSocket.send(response_line.encode())
		body = connectionSocket.recv(1024).decode().lstrip().rstrip().upper()
		
		# CASE4 PUT Request 200 OK
		if 0<len(body)<=30:
			final_response_line = "HTTP/1.1 200 OK\r\n"
			header = "Content-Type: text/html\r\n\r\n"
			response_body = f"<html><body><h1>{body}</h1></body></html>"
			response = final_response_line + header + response_body
			connectionSocket.send(response.encode())
		
		# CASE5 PUT Request 400 Bad Request
		# Cause - Body is Empty String
		else:
			final_resopnse_line = "HTTP/1.1 400 Bad Request\r\n"
			header = "Content-Type: text/html\r\n\r\n"
			response_body = f"<html><body><h1>400 Bad Request</h1></body></html>"
			response = final_resopnse_line + header + response_body
			connectionSocket.send(response.encode())
	
	# CASE6 POST Request 404 Not Found Error
	# path : /NotFoundError
	else:
		response_line = "HTTP/1.1 404 Not Found\r\n"
		header = "Content-Type: text/html\r\n\r\n"
		response_body = "<html><body><h1>404 Not Found</h1></body></html>"
		response = response_line + header + response_body
		connectionSocket.send(response.encode())
	return

def HEAD(path):
	# CASE7 HEAD Request 200 OK
	# path : /
	if path == "/":
		response_line = "HTTP/1.1 200 OK\r\n"
		header = "Content-Type: text/html\r\n\r\n"
		response = response_line + header
		connectionSocket.send(response.encode())
	
	# CASE8 HEAD Request 404 Not Found Error
	# path : /NotFoundError
	else:
		response_line = "HTTP/1.1 404 Not Found\r\n"
		header = "Content-Type: text/html\r\n\r\n"
		response_body = "<html><body><h1>404 Not Found</h1></body></html>"
		response = response_line + header + response_body
		connectionSocket.send(response.encode())
	return

def PUT(connectionSocket, message, path):
	# max file size(bytes)
	content_length = None
	headers = message.split("\r\n")
	for header in headers:
		if header.startswith("Content-Length:"):
			content_length = int(header.split(":")[1].strip())
			break
	max_size = 8192
	# CASE10 PUT Request 400 Bad Request
	# Cause - File size too large
	if content_length > max_size:
		response_line = "HTTP/1.1 400 Bad Request\r\n"
		headers = "Content-Type: text/html\r\n\r\n"
		response_body = f"<html><body><h1>400 Bad Request</h1></body></html>"
		response = response_line + headers + response_body
		connectionSocket.send(response.encode())
		return
	
	# CASE9 PUT Request 200 OK
	if "Expect: 100-Continue" in message:
		response_line = "HTTP/1.1 100 Continue\r\n\r\n"
		connectionSocket.send(response_line.encode())
		body = connectionSocket.recv(8193)
		
		if len(body) <= max_size:
			filename = path.strip("/")
			with open(filename, "wb") as file:
				file.write(body)
			response_line = "HTTP/1.1 200 OK\r\n"
			headers = "Content-Type: text/html\r\n\r\n"
			response = response_line + headers
			connectionSocket.send(response.encode())
	return
	
	
while True:
	connectionSocket, addr = serverSocket.accept()
	print("Connection from", addr)
	
	try:
		# Receive Message From Client
		message = connectionSocket.recv(1024).decode()
		print("Received request")
		print(message)
		
		# Message Parsing
		lines, request_line, method, path = request_parser(message)
		
		# Request_GET
		if method == "GET":
			GET(path)
			
		# Request_HEAD
		elif method == "HEAD":
			HEAD(path)
		
		# Request_POST
		elif method == "POST":
			# Add parameter "connectionSocket" to receive request body
			POST(connectionSocket, message, path)
		
		# Request_PUT
		elif method == "PUT":
			# Add parameter "connectionSocket" to receive request body
			PUT(connectionSocket, message, path)

		# Wrong Request (Not in [GET, POST, HEAD, PUT])
		else:
			another_request()
	
	# Server Error
	except Exception as e:
		print("Error:", e)
		response_line = "HTTP/1.1 500 Internal Server Error\r\n"
		headers = "Content-Type: text/html\r\n\r\n"
		body = "<html><head><title></title></head></html>"
		response = response_line + headers
		connectionSocket.send(response.encode())
	
	connectionSocket.close()