import socket

s = socket.socket()

s.connect(("127.0.0.1", 32017))
s.send("hello".encode())
print(s.recv(4096).decode())
s.close()
