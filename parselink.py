import json


def parse_small_data():
    file = open("facebook_combined.txt")
    result = open("facebook_conbined.json", 'w', encoding='utf-8')
    node_dict = {}
    for i in range(4039):
        node_dict[str(i)] = {
            'degree': 0,
            'inlink': [],
        }
    line = file.readline()
    while line:
        arr = line.split()
        node1 = arr[0]
        node2 = arr[1]

        node_dict[node1]['degree'] += 1
        node_dict[node1]['inlink'].append(node2)
        node_dict[node2]['degree'] += 1
        node_dict[node2]['inlink'].append(node1)

        line = file.readline()
    json.dump(node_dict, result)

if __name__ == '__main__':
    parse_small_data()