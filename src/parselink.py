import json


def parse_splited_data(infile, outfile1, outfile2, size):
    file = open(infile)
    sub_result_1 = open(outfile1, 'w', encoding='utf-8')
    sub_result_2 = open(outfile2, 'w', encoding='utf-8')
    node_dict = {}
    for i in range(size):
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

    mid = int(size / 2)
    subfile1 = {str(i): node_dict[str(i)] for i in range(mid)}
    subfile2 = {str(i): node_dict[str(i)] for i in range(mid, size)}
    json.dump(subfile1, sub_result_1)
    json.dump(subfile2, sub_result_2)


def parse_integrate_data(infile, outfile):
    file = open(infile)
    result = open(outfile, 'w', encoding='utf-8')
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
    # parse_splited_data("facebook_combined.txt", "facebook_combined_sub1.json", "facebook_combined_sub2.json", 4039)
    parse_splited_data("../data/amazon.txt", "../data/amazon_sub1.json", "../data/amazon_sub2.json", 548600)