import sys
import socket
import json

class SocketClient:
    def __init__(self, host, port):
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sckt.connect((host,port))
        msg = self.sckt.recv(1024)
        msg.decode('utf-8')
        print(msg)
        print("Successfully connected to "+str(host)+" "+str(port))

    def send_request(self, content):
        self.sckt.send(content.encode('utf-8'))

    def get_response(self):
        res = self.sckt.recv(1024)
        #print(res)
        return json.loads(res.decode('utf-8'))

    def __del__(self):
        self.sckt.close()
