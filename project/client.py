from socket import *
from sys import *


if len(argv) != 2:
    print("\n===== Error usage, python3 client.py SERVER_PORT ======\n")
    exit(0)

port=int(argv[1])

updSocket = socket(AF_INET, SOCK_DGRAM)

def upd_client():
    while True:
        # login - username
        username = input("Enter username: ")
        updSocket.sendto(username.encode(),('localhost', port))
        modifiedMessage, serverAddress = updSocket.recvfrom(2048)

        # login - password
        if modifiedMessage.decode() == 'current':
            password = input("Enter password: ")
            updSocket.sendto(password.encode(),('localhost', port))
            modifiedMessage, serverAddress = updSocket.recvfrom(2048)
            print(modifiedMessage.decode())
            # login false
            if modifiedMessage.decode() == 'Invalid password':
                continue
        elif  modifiedMessage.decode() == 'new':
            password = input("New user, enter password: ")
            updSocket.sendto(password.encode(),('localhost', port))
            modifiedMessage, serverAddress = updSocket.recvfrom(2048)
            print(modifiedMessage.decode())  
        else:
            print(modifiedMessage.decode())
            continue

        while True:
            command = input("Enter one of the following commands:"
                            "CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT: ")
            updSocket.sendto(command.encode(),('localhost', port))
            modifiedMessage, serverAddress = updSocket.recvfrom(2048)

            if 'TCP' in modifiedMessage.decode():
                command = command.lstrip(' ')
                command = command.rstrip(' ')
                command = command.split(' ')
                if 'UPD' in modifiedMessage.decode():
                    tcpSocket = socket(AF_INET, SOCK_STREAM)
                    tcpSocket.connect(('localhost', port))
                    with open(command[2], 'rb') as f:
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            tcpSocket.send(data)
                    tcpSocket.close()
                    modifiedMessage, serverAddress = updSocket.recvfrom(2048)
                if 'DWN' in modifiedMessage.decode():
                    tcpSocket = socket(AF_INET, SOCK_STREAM)
                    tcpSocket.connect(('localhost', port))
                    with open(command[2], 'wb') as f:
                        while True:
                            data = tcpSocket.recv(1024)
                            if not data:
                                break
                            f.write(data)
                    tcpSocket.close()
                    modifiedMessage, serverAddress = updSocket.recvfrom(2048)

            if modifiedMessage.decode!="":
                print(modifiedMessage.decode())
            if modifiedMessage.decode() == 'Goodbye':
                break
        break

    updSocket.close()

upd_client()