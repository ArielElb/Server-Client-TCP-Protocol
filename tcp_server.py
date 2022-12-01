import socket
import os
import sys
import os.path
from os import path

filePath = 'files/a/6.jpg'
file = None
fileContent = None
ext = os.path.splitext(filePath)[-1].lower()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(5)
while True:
    client_socket, client_address = server.accept()
    print('Connection from: ', client_address)

    data = client_socket.recv(100)
    list = data.decode('utf-8').splitlines(True)
    namePlace = False
    fileName = ''
    for x in list[0]:
        if (x == '['):
            namePlace = True
        if (x == ']'):
            namePlace = False
            if (namePlace):
                fileName = fileName + x
    if (fileName == '/'):
        fileName = "index.html"

        for l in list:

            if (l == "Connection: close"):
                close = True
                break
            if (l == "Connection: keep-alive"):
                close = False
                break

    print('Received: ', data)
    client_socket.send(data.upper())
    client_socket.close()
    print('Client disconnected')


    def fileName(line):
        namePlace = False
        fileName = ''
        for x in list[0]:
            if (x == '['):
                namePlace = True
            if (x == ']'):
                namePlace = False
                if (namePlace):
                    fileName = fileName + x
        if (fileName == '/'):
            fileName = "index.html"


    def close(list):
        for l in list:

            if (l == "Connection: close"):
                close = True
                break
            if (l == "Connection: keep-alive"):
                close = False
                break
        return close


    def hasFolderPath(name):
        for l in name:
            if (l == '/'):
                return True

    data = client_socket.recv(10000000)
    connStatus = "keep-alive"

    if filePath == 'GET /redirect HTTP/1.1':
        data = 'HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: result.html\n\n'
        client_socket.send(data.encode())
        client_socket.send(''.encode())

    if path.exists(filePath):
        # open images as binary file.
        if ext == '.jpg' or ext == '.ico' or ext == '.png':
            with open(filePath, 'rb') as file:
                fileContent = file.read()
                data = 'HTTP/1.1 200 OK\nConnection: {conn}\nContent-Length:{length}\n\n{fileContent}'.format(
                    conn=connStatus,
                    length=os.path.getsize(filePath), fileContent=fileContent)
                print ("in binary")
                client_socket.sendall(fileContent)

        else:
            with open(filePath, 'r', encoding='utf-8') as file:

                fileContent = file.read()
                data = 'HTTP/1.1 200 OK\nConnection: {conn}\nContent-Length:{length}\n\n{fileContent}'.format(
                    conn=connStatus,
                    length=os.path.getsize(filePath), fileContent=fileContent)
                client_socket.send(data.encode('utf-8'))
    # file isn't found - send 404 error.
    else:
        data = 'HTTP/1.1 404 Not Found\nConnection: {conn}\n\n'.format(
            conn="close")
        client_socket.send(data.encode())

    if connStatus == "close":
        client_socket.close()
        continue

