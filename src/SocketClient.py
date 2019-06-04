import socket

class SocketClient:
    def __init__(self, host, port):
        self.sckt = socket.socket()
        self.sckt.connect((host,port))

    def send_request(self, content):
        self.sckt.send(content)

    def get_response(self):
        return self.recv()

    def __del__(self):
        self.sckt.close()
