from collections import OrderedDict


class LimitedOrderedDict(OrderedDict):
    def __init__(self, size):
        self.size_limit = size
        OrderedDict.__init__(self)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        while len(self) > self.size_limit:
            self.popitem(last=False)


if __name__ == '__main__':
    c = LimitedOrderedDict(30)
    c.__setitem__('few', '1')
    if 'few' in c.keys():
        print(c['few'])