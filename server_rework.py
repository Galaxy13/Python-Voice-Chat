from vidstream import StreamingServer
import socket

class Server:
    def __init__(self, port=None):
        self.port = port
        self.server = StreamingServer(socket.gethostbyname(socket.gethostname()), self.port)

    def server_start(self):
        self.server.start_server()