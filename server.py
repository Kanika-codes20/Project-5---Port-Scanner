import socket
server = socket.socket()
server.bind(("127.0.0.1", 5000))
server.listen()
print("Server is listening on port 5000.....")
connection, address = server.accept()