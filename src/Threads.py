
import copy
import threading

from SocketServer import *
from SocketClient import *

alpha = 0.85
epsilon = 1e-8
max_literation = 100

local_finished = threading.Lock()
remote_finished = False
flag = False
last_node_dict = {}

class working_thread:

    def __init__(self, _node_dict, _host, _port):
        self.node_dict = _node_dict
        self.requester = SocketClient(_host, _port)
        self.port = _port
        print('Ready to work...')

    def get_node(self,id):
        if id in self.node_dict:
            return self.node_dict[id]
        else:
            #print("Asking " + id)
            if type(id) != type('1234'):
                raise AssertionError("!!!!!!!")
            self.requester.send_request(id)
            return self.requester.get_response()

    def pagerank(self):
        global remote_finished
        global flag
        global last_node_dict
        N = float(len(self.node_dict))
        iter = 0
        sample = self.get_node('0')
        pre_result = sample['rank']
        while True:
            local_finished.acquire()
            flag = True
            remote_finished = False
            iter += 1
            print('iter %d'%iter)
            index = 0
            #for k in node_dict.keys():
            for k in self.node_dict.keys():
                sum = 0
                for inlink in self.node_dict[k]['inlink']:
                    tmpnode = self.get_node(inlink)
                    sum += float(tmpnode['rank']) / float(tmpnode['degree'])
                self.node_dict[k]['rank'] = alpha * sum + (1 - alpha) / N
                index += 1
                #print('key %d iter %d' % (int(k), iter))

            result = open('../data/page_rank_'+str(self.port)+'.txt', 'w', encoding='utf-8')
            for k in self.node_dict.keys():
                result.write(k + ':' + str(self.node_dict[k]['rank']) + '\n')
                #print('write %d' % index)
                index += 1
            result.close()
            last_node_dict = self.node_dict

            local_finished.release()

            self.requester.send_request('wait')

            while not remote_finished:
                continue

            sample = self.get_node('0')
            if abs(sample['rank'] - pre_result) < epsilon:
                break
            print('iter %d delta %.*f' % (iter,10,float(abs(sample['rank'] - pre_result))))
            pre_result = sample['rank']

            if iter > max_literation:
                break

        print('iteration num: ' + str(iter))
        self.requester.send_request('end')


class datasharing_thread:

    def __init__(self, _node_dict, _port):
        self.node_dict = copy.deepcopy(_node_dict)
        self.port = _port

    def prepare(self):
        self.responser = SocketServer(self.port)
        self.responser.wait_connection()

    def wait(self):
        global remote_finished
        global flag
        global last_node_dict
        while not flag:
            continue
        while True:
            msg = self.responser.get_request()
            if msg == 'wait' :
                local_finished.acquire()
                self.node_dict = copy.deepcopy(last_node_dict)
                remote_finished = True
                local_finished.release()
            elif msg == 'end':
                break
            else:
                if not msg in self.node_dict:
                    raise AssertionError("Node "+msg+" not found.")
                self.responser.send_response(self.node_dict[msg])

    def run(self):
        self.prepare()
        self.wait()
