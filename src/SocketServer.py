import sys
import socket
import json


class SocketServer:

    def __init__(self, _port):
        self.port = _port

    def wait_connection(self):
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        self.sckt.bind((host, self.port))

        self.sckt.listen(1)
        (self.client, addr) = self.sckt.accept()
        print("Accept connection from: "+str(addr))
        #msg = self.sckt.recv(1024)
        #msg.decode('utf-8')
        msg = 'Connected to remote process.'
        msg = msg.encode('utf-8')
        self.client.send(msg)
        #print(msg)
        return

    def get_request(self):
        req = self.client.recv(99999)
        return json.loads(req.decode())

    def send_response(self, content):
        res = json.dumps(content).encode('utf-8')
        return self.client.sendall(res)

    def __del__(self):
        self.client.close()
        self.sckt.close()
