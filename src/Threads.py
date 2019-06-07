
import copy
import threading

#from src.SocketServer import *
#from src.SocketClient import *
#from src.LimitedOrderedDict import LimitedOrderedDict

from SocketServer import *
from SocketClient import *
from LimitedOrderedDict import LimitedOrderedDict

alpha = 0.85
epsilon = 1e-8
max_literation = 100
buffer_size = 300

local_finished = threading.Lock()
remote_finished = False
flag = False
last_node_dict = {}


class working_thread:

    def __init__(self, _node_dict, _host, _port, label, N):
        self.node_dict = _node_dict
        self.requester = SocketClient(_host, _port)
        self.port = _port
        self.label = label
        # self.buffer = LimitedOrderedDict(buffer_size)
        self.buffer = {}
        self.N = N
        print('Ready to work...')

    def get_node_rank(self, id):
        if id in self.node_dict:
            rank_val = self.node_dict[id]['rank'] / self.node_dict[id]['degree']
            return rank_val
        else:
            #print("Asking " + id)
            # if id in self.buffer.keys():
            #     return self.buffer[id]

            if type(id) != type('1234'):
                raise AssertionError("!!!!!!!")
            self.requester.send_request(id)
            single_dict = self.requester.get_response()
            rank_val = float(single_dict['rank']) / float(single_dict['degree'])
            # self.buffer[id] = rank_val
            # self.buffer._check_size_limit()
            return rank_val

    def pagerank(self):
        global remote_finished
        global flag
        global last_node_dict
        iter = 0
        pre_result = self.get_node_rank('0')
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
                    sum += self.get_node_rank(inlink)
                self.node_dict[k]['rank'] = alpha * sum + (1 - alpha) / self.N
                index += 1
                #print('key %d iter %d' % (int(k), iter))

            self.buffer.clear()
            result = open('../data/page_rank_' + str(self.label) + '.txt', 'w', encoding='utf-8')
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

            sample = self.get_node_rank('0')
            if abs(sample - pre_result) < epsilon:
                break
            print('iter %d delta %.*f' % (iter,10,float(abs(sample - pre_result))))
            pre_result = sample

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
                return_node = {'degree':self.node_dict[msg]['degree'], \
                                'rank':self.node_dict[msg]['rank']}
                self.responser.send_response(return_node)

    def run(self):
        self.prepare()
        self.wait()
