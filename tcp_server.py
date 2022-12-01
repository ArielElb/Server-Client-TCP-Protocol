import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 12345))
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
