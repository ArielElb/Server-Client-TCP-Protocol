import socket
import os
import sys
import os.path
from os import path

fileName = 'files/index.html'
file = None
fileContent = None
ext = os.path.splitext(fileName)[-1].lower()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)
while True:
    client_socket, client_address = server.accept()
    print('Connection from: ', client_address)
    data = client_socket.recv(100)
    print('Received: ', data.decode('utf-8'))
    connStatus = True

    if fileName == 'GET /redirect HTTP/1.1':
        data = 'HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: result.html\n\n'
        client_socket.send(data.encode())
        client_socket.send(''.encode())

    if path.exists(fileName):
        # open images as binary file.
        if ext == '.jpg' or ext == '.ico' or ext == '.png':
            with open(fileName, 'rb') as file:
                fileContent = file.read()
                client_socket.send(fileContent)
                data = 'HTTP/1.1 200 OK\nConnection: {conn}\nContent-Length:{length}\n\n{fileContent}'.format(
                    conn=connStatus,
                    length=os.path.getsize(fileName), fileContent=fileContent)
                client_socket.send(data.encode())
        else:
            with open(fileName, 'r', encoding='utf-8') as file:
                fileContent = file.read()
                client_socket.send(fileContent.encode('utf-8'))
                fileContent = file.read()
                data = 'HTTP/1.1 200 OK\nConnection: {conn}\nContent-Length:{length}\n\n{fileContent}'.format(
                    conn=connStatus,
                    length=os.path.getsize(fileName), fileContent=fileContent)
                client_socket.send(data.encode())
    # file isn't found - send 404 error.
    else:
        data = 'HTTP/1.1 404 Not Found\nConnection: {conn}\n\n'.format(
            conn="close")
        client_socket.send(data.encode())

    client_socket.close()
    print('Client disconnected')
