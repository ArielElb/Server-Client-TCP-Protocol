import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 12345))
s.send('hello baby\n'.encode('utf-8'))
data = s.recv(1000)
print("Server sent: ", data.decode('utf-8'))
s.close()