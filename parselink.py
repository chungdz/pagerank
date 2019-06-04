import json


def parse_small_data(infile, outfile1, outfile2):
    file = open(infile)
    sub_result_1 = open(outfile1, 'w', encoding='utf-8')
    sub_result_2 = open(outfile2, 'w', encoding='utf-8')
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

    subfile1 = {str(i): node_dict[str(i)] for i in range(2020)}
    subfile2 = {str(i): node_dict[str(i)] for i in range(2020, 4039)}
    json.dump(subfile1, sub_result_1)
    json.dump(subfile2, sub_result_2)

if __name__ == '__main__':
    parse_small_data("facebook_combined.txt", "facebook_combined_sub1.json", "facebook_combined_sub2.json")