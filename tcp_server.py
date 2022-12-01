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

def getPath(fileName):
    if fileName.startswith("files"):
        return fileName
    if fileName == '' or fileName == '/':
        return fileName + 'files/index.html'
    else:
        return 'files/' + fileName

while True:
    client_socket, client_address = server.accept()
    print('Connection from: ', client_address)
    client_socket.settimeout(1)
    data = client_socket.recv(1000)
    fileLines = data.decode('utf-8').splitlines(True)
    filePath = getPath(fileName(fileLines[0]))
    ext = os.path.splitext(filePath)[-1].lower()
    connStatus = close(fileLines)

    if filePath == '/redirect':
        data = 'HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: result.html\n\n'
        print(data)
        client_socket.send(data.encode())
        client_socket.send(''.encode())

    # if filePath == '/':
    #     filePath = 'files/index.html'
    if path.exists(filePath):
        # open images as binary file.
        if ext == '.jpg' or ext == '.ico' or ext == '.png':
            with open(filePath, 'rb') as file:

                fileContent = file.read()
                data = 'HTTP/1.1 200 OK\nContent-Type: image/jpeg\nContent-Length: ' + str(len(fileContent)) + '\n\n'
                print(data + str(fileContent))
                encodeData = data.encode()
                client_socket.send(encodeData + fileContent)
        else:
            with open(filePath, 'r', encoding='utf-8') as file:
                fileContent = file.read()
                data = 'HTTP/1.1 200 OK\nConnection: {conn}\nContent-Length:{length}\n\n {fileContent}'.format(
                    conn=connStatus,
                    length=os.path.getsize(filePath), fileContent=fileContent)
                print(data)
                client_socket.send(data.encode('utf-8'))
    # file isn't found - send 404 error.
    else:
        data = 'HTTP/1.1 404 Not Found\nConnection: {conn}\n\n'.format(
            conn="close")
        print(data)
        client_socket.send(data.encode())
        client_socket.send(''.encode())

    if connStatus == "close":
        client_socket.close()
        continue
