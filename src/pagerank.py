import json
import argparse
import socket
import os
import _thread
N = 4038
alpha = 0.85
epsilon = 1e-10

from Threads import *

def main():
    local_host = socket.gethostname()
    #parse arguments
    parser = argparse.ArgumentParser(description='Toy distributed pagrank program.')
    parser.add_argument('-d', '--data', type=str, help='Data you want to pagerank.', default = 'data/facebook_combined.json')
    parser.add_argument('-sp', '--sport', type=int, help='Port your data-sharing thread use.')
    parser.add_argument('-wh', '--whost', type=str, help='Host your working thread try to contact.', default = local_host)
    parser.add_argument('-wp', '--wport', type=int, help='Port your working thread try to contact.')

    args = parser.parse_args()

    file = open(args.data, 'r', encoding='utf-8')
    node_dict = json.load(file)
    file.close()
    # Initialize 'rank'
    N = float(len(node_dict))
    index = 0
    for k in node_dict.keys():
        node_dict[k]['rank'] = 1.0 / N
        index += 1
        print('init %d node, id: %d'%(index,int(k)))
    print('Initicalizing nodes finished.')

    dst = datasharing_thread(node_dict, args.sport)
    _thread.start_new_thread ( dst.run, () )

    print("Ready to connect to another process...")
    input()
    wt = working_thread(node_dict, args.whost, args.wport)
    wt.pagerank()


if __name__ == '__main__':
    main()