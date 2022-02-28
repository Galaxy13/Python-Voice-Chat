#!/usr/bin/python3

import socket
import threading
import pyaudio

class Client:
    def __init__(self, server_ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # while 1:
        #     try:
        self.target_ip = server_ip
        self.target_port = port
        self.connected = 0

                # self.s.connect((self.target_ip, self.target_port))

            #     break
            # except:
            #     return ("Couldn't connect to server")

        # chunk_size = 1024 # 512
        # audio_format = pyaudio.paInt16
        # channels = 1
        # rate = 20000
        #
        # # initialise microphone recording
        # self.p = pyaudio.PyAudio()
        # self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        # self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        #
        # print("Connected to Server")
        #
        # # start threads
        # receive_thread = threading.Thread(target=self.receive_server_data).start()
        # self.send_data_to_server()

    def client_launch(self):
        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        print("Connected to Server")

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        # self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass


    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass


    def connect(self):
        try:
            self.s.connect((self.target_ip, int(self.target_port)))
            self.connected = 1
        except:
            return

# client = Client()
