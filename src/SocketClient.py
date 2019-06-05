import sys
import socket
import json

class SocketClient:
    def __init__(self, host, port):
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sckt.connect((host,port))

        #msg = 'Connected to remote process.'
        #self.sckt.send(msg.encode('utf-8'))
        msg = self.sckt.recv(1024)
        msg = msg.decode()
        print(msg)
        print("Successfully connected to "+str(host)+" "+str(port))

    def send_request(self, content):
        #print(content)
        self.sckt.send(content.encode('utf-8'))

    def get_response(self):
        res = self.sckt.recv(10000)
        #print(res)
        return json.loads(res.decode())

    def __del__(self):
        self.sckt.close()
