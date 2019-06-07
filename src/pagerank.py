import json
import argparse
import socket
import os
import _thread
alpha = 0.85
epsilon = 1e-10

from src.Threads import *

def main():
    local_host = socket.gethostname()
    #parse arguments
    parser = argparse.ArgumentParser(description='Toy distributed pagrank program.')
    parser.add_argument('-d', '--data', type=str, help='Data you want to pagerank.', default = 'data/facebook_combined.json')
    parser.add_argument('-sp', '--sport', type=int, help='Port your data-sharing thread use.')
    parser.add_argument('-wh', '--whost', type=str, help='Host your working thread try to contact.', default = local_host)
    parser.add_argument('-wp', '--wport', type=int, help='Port your working thread try to contact.')
    parser.add_argument('-chp', '--checkpoint', type=int, help='whether to use saved page rank', default=0)
    parser.add_argument('-num', '--node_number', type=float, default=4038)

    args = parser.parse_args()

    file = open(args.data, 'r', encoding='utf-8')
    node_dict = json.load(file)
    file.close()
    # Initialize 'rank'
    N = args.node_number
    index = 0
    for k in node_dict.keys():
        node_dict[k]['rank'] = 1.0 / N
        index += 1
        # print('init %d node, id: %d' % (index, int(k)))
    if args.checkpoint == 1:
        url = '../data/page_rank_' + str(args.sport) + '.txt'
        rankfile = open(url, 'r', encoding='utf-8')
        line = rankfile.readline()
        while line:
            arr = line.split(':')
            key_str = arr[0]
            val = float(arr[1])
            node_dict[key_str]['rank'] = val
            line = rankfile.readline()
    print('Initicalizing nodes finished.')

    dst = datasharing_thread(node_dict, args.sport)
    _thread.start_new_thread(dst.run, ())

    print("Ready to connect to another process...")
    input()
    wt = working_thread(node_dict, args.whost, args.wport, args.sport, N)
    wt.pagerank()


if __name__ == '__main__':
    main()
