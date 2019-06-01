import json
N = 4038
alpha = 0.85
epsilon = 1e-10


def page_rank(url):
    file = open(url, 'r', encoding='utf-8')
    node_dict = json.load(file)
    iter = 0
    print('init')
    index = 0

    for k in node_dict.keys():
        node_dict[k]['rank'] = 1 / N
        index += 1
        print('init %d'%index)

    pre_result = node_dict['0']['rank']
    while True:
        iter += 1
        print('iter %d'%iter)
        index = 0
        for k in node_dict.keys():
            sum = 0
            for inlink in node_dict[k]['inlink']:
                sum += node_dict[inlink]['rank'] / node_dict[inlink]['degree']
            node_dict[k]['rank'] = alpha * sum + (1 - alpha) / N
            index += 1
            print('key %d iter %d' % (index, iter))

        if abs(node_dict['0']['rank'] - pre_result) < epsilon:
            break

        pre_result = node_dict['0']['rank']

        if iter > 100:
            break

    result = open('page_rank.txt', 'w', encoding='utf-8')
    index = 0
    for k in node_dict.keys():
        result.write(k + ':' + str(node_dict[k]['rank']) + '\n')
        print('write %d' % index)
        index += 1
    result.close()
    file.close()
    print('iteration num: ' + str(iter))


if __name__ == '__main__':
    page_rank('facebook_combined.json')
