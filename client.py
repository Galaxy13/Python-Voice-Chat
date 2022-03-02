#!/usr/bin/python3

import socket
import threading
import pyaudio

chunk_size = 1024  # 512
audio_format = pyaudio.paInt16
channels = 1
rate = 20000


class Client:
    def __init__(self, server_ip=None, port=None):
        # initialize pyAudio object
        self.p = pyaudio.PyAudio()
        # initialize device dictionary
        self.input_devices = {}
        self.output_devices = {}
        self.device_list()

        # initialise microphone recording and audio streaming
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # socket parameters
        self.target_ip = server_ip
        self.target_port = port
        self.connected = 0

    def client_launch(self):
        print("Connected to Server")

        # Threads start
        threading.Thread(target=self.receive_server_data).start()
        threading.Thread(target=self.send_data_to_server).start()

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

    def device_list(self):
        info = self.p.get_host_api_info_by_index(0)
        for index in range(0, info.get('deviceCount')):
            if (self.p.get_device_info_by_host_api_device_index(0, index)).get('maxInputChannels') > 0:
                self.input_devices[self.p.get_device_info_by_host_api_device_index(0, index).get('name')] = index
            if self.p.get_device_info_by_host_api_device_index(0, index).get('maxOutputChannels') > 0:
                self.output_devices[self.p.get_device_info_by_host_api_device_index(0, index).get('name')] = index

    def set_input_device(self, input_index):
        self.recording_stream.close()
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size, input_device_index=input_index)

    def set_output_device(self, output_index):
        self.playing_stream.close()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size, output_device_index=output_index)

    def set_target_ip(self, ip_address):
        self.target_ip = ip_address

    def set_port(self, port):
        self.target_port = int(port)

    def input_stop(self):
        self.recording_stream.stop_stream()

    def input_start(self):
        self.recording_stream.start_stream()

    def output_stop(self):
        self.playing_stream.stop_stream()

    def output_start(self):
        self.playing_stream.start_stream()
