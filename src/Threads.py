
import copy

from SocketServer import *
from SocketClient import *

alpha = 0.85
epsilon = 1e-10
max_literation = 100

local_finished = False
remote_finished = False
last_node_dict = {}

class working_thread:

    def __init__(self, _node_dict, _host, _port):
        self.node_dict = _node_dict
        self.host = _host
        self.port = _port

    def prepare(self):
        self.requester = SocketClient(self.host, self.port)
        print('Ready to work...')

    def get_node(self,id):
        if id in self.node_dict:
            return self.node_dict[id]
        else:
            self.requester.send_request(id)
            return self.requester.get_response()

    def pagerank(self):
        N = float(len(self.node_dict))
        iter = 0
        index = 0
        strt = ''
        for k in self.node_dict.keys():
            self.node_dict[k]['rank'] = 1.0 / N
            if index == 0:
                strt = k
            index += 1
            print('init %d node, id: %d'%(index,int(k)))
        print('Initicalizing nodes finished.')

        pre_result = self.node_dict[strt]['rank']
        while True:
            local_finished = False
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
                print('key %d iter %d' % (index, iter))

            if abs(self.node_dict[strt]['rank'] - pre_result) < epsilon:
                break

            pre_result = self.node_dict[strt]['rank']

            if iter > max_literation:
                break

            result = open('page_rank_'+strt+'.txt', 'w', encoding='utf-8')
            for k in self.node_dict.keys():
                result.write(k + ':' + str(self.node_dict[k]['rank']) + '\n')
                #print('write %d' % index)
                index += 1
            result.close()
            last_node_dict = self.node_dict
            local_finished = True
            self.requester.send_request('wait')
            while not remote_finished:
                continue
        print('iteration num: ' + str(iter))
        self.requester.send_request('end')

    def run(self):
        self.prepare()
        input()
        self.pagerank()


class datasharing_thread:

    def __init__(self, _node_dict, _port):
        self.node_dict = copy.deepcopy(_node_dict)
        self.port = _port

    def prepare(self):
        self.responser = SocketServer(self.port)
        self.responser.wait_connection()

    def wait(self):
        while True:
            msg = self.responser.get_request()
            if msg == 'wait' :
                while not local_finished:
                    continue
                self.node_dict = copy.deepcopy(last_node_dict)
                remote_finished = True

            elif msg == 'end':
                break
            else:
                if msg in self.node_dict:
                        print(self.node_dict[msg])
                        self.responser.send_response(self.node_dict[msg])
                else:
                    print("No node founded.")
                    SimError("No node founded.")
    def run(self):
        self.prepare()
        self.wait()
