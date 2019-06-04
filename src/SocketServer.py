import sys
import socket

class SocketServer:

    def __init__(self, _port):
        self.port = _port


    def wait_connection(self):
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        self.sckt.bind((host, self.port))
        self.sckt.listen(5)
        (client,addr) = self.sckt.accept()
        print("Accept connection from: "+str(addr))
        msg = 'Connected to remote process.'
        self.sckt.send(msg.encode('utf-8'))
        return

    def get_request(self):
        req = self.sckt.recv(1024)
        return req.decode('utf-8')

    def send_response(self, content):
        return self.sckt.send(content.encode('utf-8'))

    def __del__(self):
        self.sckt.close()
