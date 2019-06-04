import socket

class SocketServer:

    def __init__(self, port):
        self.sckt = socket.socket()
        host = socket.gethostname()
        self.sckt.bind((host, port))
        self.sckt.listen(1)
        self.node_dict

    def wait_connection(self):
        client,addr = self.sckt.accept()
        print("Accept connection from: "+addr)
        return client, addr

    def get_request(self):
        return self.sckt.recv()

    def send_response(self, content):
        return self.sckt.send(content)

    def __del__(self):
        self.sckt.close()
