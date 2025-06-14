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
            print(modifiedMessage.decode())
            if modifiedMessage.decode() == 'Goodbye':
                break
        break

    updSocket.close()

upd_client()