import socket
import os
import sys
import os.path
from os import path


def fileName(line):
    names = line.split(' ')
    name = names[1]
    fileName = name[1:]
    return fileName


def close(list):
    for l in list:
        if l == 'Connection: close':
            return "close"
        if l == "Connection: keep-alive":
            return "keep-alive"


def getPath(fileName):
    if fileName.startswith("files"):
        return fileName
    if fileName == '' or fileName == '/':
        return fileName + 'files/index.html'
    else:
        return 'files/' + fileName


def runServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((sys.argv[1], 8080))
    server.listen(5)
    while True:
        try:
            client_socket, client_address = server.accept()
            client_socket.settimeout(1)
            data = client_socket.recv(1000)
            client_socket.settimeout(None)
            fileLines = data.decode('utf-8').splitlines(True)
            lastLine = fileLines[-1]
            fileLines = data.decode('utf-8').splitlines()
            filePath = getPath(fileName(fileLines[0]))
            ext = os.path.splitext(filePath)[-1].lower()
            connStatus = close(fileLines)
        except:
            print('Connection closed : timeout')
            client_socket.close()
            continue
        if filePath == 'files/redirect':
            data = 'HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: /result.html\n\n' + ''
            connStatus = 'close'
            client_socket.send(data.encode())
            print(data)
        elif path.exists(filePath):
            # open images as binary file.
            if ext == '.jpg' or ext == '.ico' or ext == '.png':
                with open(filePath, 'rb') as file:
                    fileContent = file.read()
                    data = f'HTTP/1.1 200 OK\nConnection:{connStatus} \nContent-Length: ' + str(len(fileContent)) + '\n\n'
                    print(data)
                    print(fileContent )
                    print('\n')
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
            connStatus = 'close'
            client_socket.send(data.encode())
            client_socket.send(''.encode())


        if connStatus == "close":
            client_socket.close()
            continue



def main():
    runServer()


if __name__ == "__main__":
    main()
