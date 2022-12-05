import socket
import os
import sys
import os.path
from os import path


def fileName(line):
    names = line.split(' ')
    name = names[1]
    fName = name[1:]
    return fName


def check_conn_status(list):
    if 'Connection: close' in list:
        return 'close'
    if 'Connection: keep-alive' in list:
        return 'keep-alive'


def getPath(fName):
    if fName.startswith("files"):
        return fName
    if fName == '' or fName == '/':
        return fName + 'files/index.html'
    else:
        return 'files/' + fName


def redirect(client_socket):
    data = 'HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: /result.html\r\n\r\n'
    client_socket.send(data.encode())
    print(data)
    return 'close'


def send_img(client_socket, filePath, connStatus):
    with open(filePath, 'rb') as file:
        fileContent = file.read()
        data = f'HTTP/1.1 200 OK\nConnection:{connStatus} \nContent-Length: ' + str(
            len(fileContent)) + '\n\n'
        print(data)
        print(fileContent)
        print('\n')
        encodeData = data.encode()
        client_socket.send(encodeData + fileContent)


def send_default_data(client_socket, filePath, connStatus):
    with open(filePath, 'r', encoding='utf-8') as file:
        fileContent = file.read()
        data = 'HTTP/1.1 200 OK\nConnection: {conn}\nContent-Length:{length}\n\n {fileContent}'.format(
            conn=connStatus,
            length=os.path.getsize(filePath), fileContent=fileContent)
        print(data)
        client_socket.send(data.encode('utf-8'))


def error_404(client_socket, connStatus):
    data = 'HTTP/1.1 404 Not Found\nConnection: {conn}\r\n\r\n'.format(
        conn="close")
    print(data)
    connStatus = 'close'
    client_socket.send(data.encode())
    return connStatus


def run_server():
    client_socket = None
    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server.bind((sys.argv[1], 8080))
    # Listen for incoming connections
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
            connStatus = check_conn_status(fileLines)

            if filePath == 'files/redirect':
                connStatus = redirect(client_socket)
            elif path.exists(filePath):
                # open images as binary file.
                if ext == '.jpg' or ext == '.ico' or ext == '.png':
                    send_img(client_socket, filePath, connStatus)
                else:
                    send_default_data(client_socket, filePath, connStatus)
            # file isn't found - send 404 error.
            else:
                connStatus = error_404(client_socket, connStatus)

            if connStatus == "close":
                client_socket.close()
                print("closed")
                continue
        except:
            print('Connection closed : timeout')
            client_socket.close()
            continue


def main():
    run_server()


if __name__ == "__main__":
    main()
