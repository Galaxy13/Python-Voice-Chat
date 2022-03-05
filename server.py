#!/usr/bin/python3

import socket
import threading

HEADER = 64
FORMAT = 'utf-8'

class Server:
    def __init__(self):
            self.ip = socket.gethostbyname(socket.gethostname())
            while 1:
                try:
                    self.port = int(input('Enter port number to run on --> '))

                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.bind((self.ip, self.port))

                    break
                except:
                    print("Couldn't bind to that port")

            self.connections = []
            self.accept_connections()

    def accept_connections(self):
        self.s.listen(100)

        print('Running on IP: '+self.ip)
        print('Running on port: '+str(self.port))
        
        while True:
            c, addr = self.s.accept()

            self.connections.append(c)

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()
        
    def broadcast(self, sock, data, data_type):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data_type.encode(FORMAT))
                    if data_type == 'V':
                        client.send(data)
                    elif data_type == 'C':
                        data = data.encode(FORMAT)
                        msg_length = len(data)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length = b' ' * (HEADER - len(send_length))
                        client.send(send_length)
                        client.send(data)
                except:
                    pass

    def handle_client(self,c,addr):
        connected = True
        while connected:
            try:
                msg_type = c.recv(128).decode(FORMAT)
                if msg_type == 'V':
                    data = c.recv(1024)
                    self.broadcast(c, data, 'V')
                elif msg_type == 'C':
                    msg_length = self.c.recv(HEADER).decode(FORMAT)
                    msg_length = int(msg_length)
                    msg = self.c.recv(msg_length).decode(FORMAT)

            
            except socket.error:
                c.close()

server = Server()
