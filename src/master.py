import sys
import socket
import json
import threading
from threading import Condition, Lock, Event


class SocketServer:

    def __init__(self, _port, worker, buffer=0):
        self.port = _port
        self.worker = worker
        if buffer != 0:
            self.buffer = buffer
        else:
            self.buffer = worker - 1

        self.thread_points = []
        for i in range(worker):
            self.thread_points.append({
                'producer': None,
                'consumer': None,
                'tasks': 0,
                'task_buffer': [],
                'condition': Condition(),
                'event': Event()
            })

    def wait_connection(self):
        preprared_worker = 0
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        self.sckt.bind((host, self.port))

        self.sckt.listen(self.worker * 2)
        while True:
            new_client, addr = self.sckt.accept()
            print("Accept connection from: " + str(addr))
            worker_msg = self.get_request(new_client)
            worker_id = worker_msg['id']
            worker_type = worker_msg['type']
            self.thread_points[worker_id][worker_type] = new_client
            preprared_worker += 1
            if preprared_worker == self.worker * 2:
                break
        return

    @staticmethod
    def get_request(client, len=99999):
        req = client.recv(len)
        return json.loads(req.decode())

    @staticmethod
    def send_response(client, content):
        res = json.dumps(content).encode('utf-8')
        return client.sendall(res)

    def __del__(self):
        self.client.close()
        self.sckt.close()
