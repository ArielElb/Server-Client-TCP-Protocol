import socket
import os
import sys
import os.path
from os import path

filePath = ''
file = None
fileContent = None
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(5)


def fileName(line):
    names = line.split(' ')
    name = names[1]
    fileName = name[1:]
    return fileName

def close(list):
    for l in list:
        if l == "Connection: close":
            close = "close"
            return close
        if l == "Connection: keep-alive":
            return "keep-alive"



while True:
    client_socket, client_address = server.accept()
    print('Connection from: ', client_address)
    data = client_socket.recv(1000)
    fileLines = data.decode('utf-8').splitlines(True)
    filePath = fileName(fileLines[0])
    ext = os.path.splitext(filePath)[-1].lower()
    connStatus = close(fileLines)

    if filePath == 'GET /redirect HTTP/1.1':
        data = 'HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: result.html\n\n'
        client_socket.send(data.encode())
        client_socket.send(''.encode())

    if filePath == '/':
        filePath = 'files/index.html'
    if path.exists(filePath):
        # open images as binary file.
        if ext == '.jpg' or ext == '.ico' or ext == '.png':
            with open(filePath, 'rb') as file:

                fileContent = file.read()
                data = 'HTTP/1.1 200 OK\nContent-Type: image/jpeg\nContent-Length: ' + str(len(fileContent)) + '\n\n'
                encodeData = data.encode()
                client_socket.send(encodeData + fileContent)
        else:
            with open(filePath, 'r', encoding='utf-8') as file:
                fileContent = file.read()
                temp = 'HTTP/1.1 200 OK\nConnection: {conn}\nContent-Length:{length} \n\n'.format(conn = connStatus, length = os.path.getsize(filePath))
                data = temp.encode('utf-8') + fileContent.encode('utf-8')
                finalData = data.encode('utf-8')
                # data = 'HTTP/1.1 200 OK\nConnection: {conn}\nContent-Length:{length}\n\n{fileContent}'.format(
                #     conn=connStatus,
                #     length=os.path.getsize(filePath), fileContent=fileContent)
                client_socket.send(finalData)
    # file isn't found - send 404 error.
    else:
        data = 'HTTP/1.1 404 Not Found\nConnection: {conn}\n\n'.format(
            conn="close")
        client_socket.send(data.encode())

    if connStatus == "close":
        client_socket.close()
        continue
