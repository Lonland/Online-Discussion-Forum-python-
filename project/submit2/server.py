from queue import Queue
from socket import *
from sys import *
from threading import Thread
import os

login_user = []
users = {}
threads = []
messages = {}
created = {}

def get_users():
    with open('credentials.txt', 'r') as f:
        for line in f:
            text=line.split(' ')
            text[1]=text[1].rstrip('\n')
            users[text[0]]=text[1]

def test_username(username):
    print("Client authenticating")
    
    if username in login_user:
        return f"{username} has already logged in"
    if username in users.keys():
        return "current"
    return "new"

def login(username, password):
    if username not in users.keys():
        print("New user")
        print(f"{username} successfully logged in")
        users[username]=password
        with open('credentials.txt', 'a') as f:
            f.write(f"\n{username} {password}")
        return ""

    if users[username]==password:
        login_user.append(username)
        print(f"{username} successful login")
        return "Welcome to the forum"
    else:
        print("Incorrect password")
        return "Invalid password"
     
def do_command(username, command): # CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT
    command_list = ['CRT', 'MSG', 'DLT', 'EDT', 'LST', 'RDT', 'UPD', 'DWN', 'RMV', 'XIT']
    if command[0] not in command_list:
        return 'Invalid command'
    
    # XIT
    if 'XIT' == command[0]:
        if len(command)!=1:
            return "Incorrect syntax for XIT"
        print(f"{username} exited")
        login_user.remove(username)
        return 'Goodbye'
    
    # CRT: CRT threadtitle
    if 'CRT' == command[0]:
        if len(command)!=2:
            return "Incorrect syntax for CRT"
        
        print(f"{username} issued {command[0]} command")
        thread = command[1]
        if thread in threads:
            print(f"Thread {thread} exists")
            return f"Thread {thread} exists"
        print(f"Thread {thread} created")
        threads.append(thread)
        created[thread] = username
        messages[thread] = []
        return f"Thread {thread} created"
    
    # MSG: MSG threadtitle message 
    if 'MSG' == command[0]:
        if len(command)<3:
            return "Incorrect syntax for MSG"
        print(f"{username} issued {command[0]} command")
        
        if command[1] not in threads:
            print("[MSG]: no thread")
            return "[MSG]: no thread"
        cnt = len([msg for msg in messages[command[1]] if msg[0] > 0]) + 1
        messages[command[1]].append((cnt, username, ' '.join(command[2:])))
        print(f"Message posted to {command[1]} thread")
        return f"Message posted to {command[1]} thread"
    
    # DLT threadtitle messagenumber
    if 'DLT' == command[0]:
        if len(command)!=3:
            return "Incorrect syntax for DLT"
        print(f"{username} issued {command[0]} command")
        if command[1] not in threads:
            print("[DLT]: no thread")
            return "[DLT]: no thread"
        flag = False
        for i in range(len(messages[command[1]])):
            msg = messages[command[1]][i]
            if flag and msg[0]>0:
                messages[command[1]][i][0] -= 1
                continue
            if msg[0]==int(command[2]):
                if username == msg[1]:
                    messages[command[1]].pop(msg)
                    print("Message has been deleted")
                    flag = True
                else:    
                    print("Message cannot be deleted")
                    return "The message belongs to another user and cannot be edited"
        if flag:
            return "The message has been deleted"
        else:
            return "[DLT] No such message can be deleted"
    
    # EDT threadtitle messagenumber message
    if 'EDT' == command[0]:
        if len(command)<4:
            return "Incorrect syntax for EDT"
        print(f"{username} issued {command[0]} command")
        if command[1] not in threads:
            print("[DLT]: no thread")
            return "[DLT]: no thread"
        for i in range(len(messages[command[1]])):
            msg = messages[command[1]][i]
            if msg[0]==int(command[2]):
                if username == msg[1]:
                    messages[command[1]][i][2] = command[3:]
                    print("Message has been edited")
                    return "The message has been edited"
                else:    
                    print("Message cannot be edited")
                    return "The message belongs to another user and cannot be edited"
        return "[EDT] No such message can be edited"

    # LST 
    if 'LST' == command[0]:
        if len(command)!=1:
            return "Incorrect syntax for LST"
        print(f"{username} issued {command[0]} command")
        if len(threads) == 0:
            return 'No threads to list'
        else:
            join_threads = '\n'.join(threads)
            return f"The list of active threads:\n{join_threads}"
    
    # RDT threadtitle
    if 'RDT' == command[0]:
        if len(command)!=2:
            return "Incorrect syntax for RDT"
        print(f"{username} issued {command[0]} command")
        
        if len(command)>2 or command[1] not in threads:
            print("Incorrect thread specified")
            return f"Thread {command[1]} does not exist"
        
        print(f"Thread {command[1]} read")
        if len(messages[command[1]])==0:
            return f"Thread {command[1]} is empty"
        else:
            lines = []
            for msg in messages[command[1]]:
                if msg[0]>0:
                    lines.append(f"{msg[0]} {msg[1]}: {msg[2]}")
                else:
                    lines.append(msg[2])
            all_message = '\n'.join(lines)
            return all_message
    
    # RMV threadtitle
    if 'RMV' == command[0]:
        if len(command)!=2:
            return "Incorrect syntax for RMV"
        print(f"{username} issued {command[0]} command")
        if command[1] not in threads:
            print("Incorrect thread specified")
            return f"Thread {command[1:]} does not exist"
        if created[command[1]] != username:
            print(f"Thread {command[1]} cannot be removed")
            return "The thread was created by another user and cannot be removed"
        created.pop(command[1])
        messages.pop(command[1])
        threads.remove(command[1])
        print(f"Thread {command[1]} removed")
        return "The thread has been removed"
    
    # UPD threadtitle filename 
    if 'UPD' == command[0]:
        if len(command)!=3:
            return "Incorrect syntax for UPD"
        print(f"{username} issued {command[0]} command")
        if command[1] not in threads:
            return "[UPD]: no such thread"
        target_filename = f"{command[1]}-{command[2]}"
        if os.path.exists(target_filename):
            return "[UPD]: In the thread already exists this file"
        messages[command[1]].append((0, username, f"{username} uploaded file {command[2]} to {command[1]} thread"))
        return f"TCP-UPD {target_filename}"
        
    # DWN threadtitle filename
    if 'DWN' == command[0]:
        if len(command)!=3:
            return "Incorrect syntax for DWN"
        print(f"{username} issued {command[0]} command")
        if command[1] not in threads:
            return "[DWN]: no such thread"
        target_filename = f"{command[1]}-{command[2]}"
        if not os.path.exists(target_filename):
            return "[DWN]: In the thread do not exists this file"
        return f"TCP-DWN {target_filename}"
                

if len(argv) != 2:
    print("\n===== Error usage, python3 server.py SERVER_PORT ======\n")
    exit(0)
port=int(argv[1])
get_users()

# Create UDP socket
updSocket = socket(AF_INET, SOCK_DGRAM)
updSocket.bind(('localhost', port))
print("Waiting for clients")


class ClientThread(Thread):
    def __init__(self, clientAddress):
        Thread.__init__(self)
        self.clientAddress = clientAddress
        self.message_queue = Queue()
        self.clientAlive = False
        
        # print("===== New connection created for: ", clientAddress)
        self.clientAlive = True
    
    def receive_message(self):
        self.message = self.message_queue.get()

    
    def run(self):
        while self.clientAlive:
            # Get username
            self.receive_message()
            username = self.message
            self.message = ""
            reply = test_username(username)
            updSocket.sendto(reply.encode(), self.clientAddress)
            # user logged in
            if reply == f"{username} has already logged in":
                continue
            
            # Get password
            self.receive_message()
            password = self.message
            self.message = ""
            reply = login(username, password)
            if reply != "":
                updSocket.sendto(reply.encode(), self.clientAddress)
            # Password wrong
            if reply == 'Invalid password':
                continue

            # Get command
            while True:
                self.receive_message()
                command = self.message
                self.message = ""
                command = command.lstrip(' ')
                command = command.rstrip(' ')
                command = command.split(' ')
                reply = do_command(username, command)
                updSocket.sendto(reply.encode(), self.clientAddress)
                if reply == 'Goodbye':
                    break

                if 'TCP-UPD' in reply:
                    sp_re = reply.split(' ')
                    target_filename = sp_re[1]
                    tcpSocket = socket(AF_INET, SOCK_STREAM)
                    tcpSocket.bind(('localhost', port))
                    tcpSocket.listen(1)
                    conn, addr = tcpSocket.accept()
                    with open(target_filename, 'wb') as f:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            f.write(data)
                    conn.close()
                    tcpSocket.close()
                    print(f"{username} uploaded file {command[2]} to {command[1]} thread")
                    reply = f"{command[2]} uploaded to {command[1]} thread"
                    updSocket.sendto(reply.encode(), self.clientAddress)
                if 'TCP-DWN'in reply:
                    sp_re = reply.split(' ')
                    target_filename = sp_re[1]
                    tcpSocket = socket(AF_INET, SOCK_STREAM)
                    tcpSocket.bind(('localhost', port))
                    tcpSocket.listen(1)
                    conn, addr = tcpSocket.accept()
                    with open(target_filename, 'rb') as f:
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            conn.send(data)
                    conn.close()
                    tcpSocket.close()
                    print(f"{command[2]} download fromed Thread {command[1]}")
                    reply =  f"{command[2]} successfully downloaded"
                    updSocket.sendto(reply.encode(), self.clientAddress)

            print("Waiting for clients")

adr_thread = {}
while True:
    message, adr = updSocket.recvfrom(2048)
    # print(message, adr)
    if adr not in adr_thread:
        clientThread = ClientThread(adr)
        clientThread.start()
        adr_thread[adr] = clientThread
    adr_thread[adr].message_queue.put(message.decode())