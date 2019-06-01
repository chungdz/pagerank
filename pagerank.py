import json
N = 4038
alpha = 0.85
epsilon = 1e-10


def loadjson(url, input='', frombegin=True):
    file = open(url)
    phasedict = json.load(file)
    iter = 0
    print('init')
    index = 0
    if frombegin == False:
        input = open(input, encoding='utf-8')

    for k in phasedict.keys():
        phasedict[k]['pi'] = 1 / N
        index += 1
        print('init %d'%index)


    if frombegin == False:
        line = input.readline()
        index = 0
        while line:
            pair = line.split(':')
            num = float(pair[-1])
            title = ':'.join(pair[0:-1])
            phasedict[title]['pi'] = num
            index += 1
            line = input.readline()
            print('init_from_pre %d'%index)

    pre_result = phasedict['Canada']['pi']
    while True:
        iter += 1
        print('iter %d'%iter)
        index = 0
        for k in phasedict.keys():
            sum = 0
            for inlink in phasedict[k]['inlink']:
                sum += phasedict[inlink]['pi'] / phasedict[inlink]['outlinknum']
            phasedict[k]['pi'] = alpha * sum + (1 - alpha) / N
            index += 1
            print('key %d iter %d' % (index, iter))

        if abs(phasedict['Canada']['pi'] - pre_result) < epsilon:
            break

        if iter > 40:
            break

    result = open('final_result2.txt', 'w', encoding='utf-8')
    index = 0
    for k in phasedict.keys():
        result.write(str(k) + ':' + str(phasedict[k]['pi']) + '\n')
        print('write %d' % index)
        index += 1
    result.close()
    file.close()
    print('iteration num: ' + str(iter))


if __name__ == '__main__':
    loadjson('pagesinfo2.json', input='pre.txt', frombegin=False)
    # loadjson('pagesinfo2.json')
