# coding:utf-8

import math
from math import log, e
import redis
import hashlib
from hashlib import md5


class SimpleHash(object):

    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(value.__len__()):
            ret += self.seed*ret + ord(value[i])
        return (self.cap-1) & ret


class MyBloomFilter(object):
    def __init__(self, host='localhost', port=6379, db=0, key=None, blocknum=1, bit_size=1 << 20):
        self.sever = redis.StrictRedis(host=host, port=port, db=db)
        self.bit_size = bit_size
        self.seeds = [3, 5, 7, 11, 13, 31, 67]
        if key is None:
            self.key = 'test_key'
        else:
            self.key = key
        self.blockNum = blocknum
        self.hashFunc = []
        for seed in self.seeds:
            self.hashFunc.append(SimpleHash(self.bit_size, seed))

    def is_contains(self, str_input, key=None):
        if not key:
            key = self.key
        if not str_input:
            return False
        m5 = md5()
        m5.update(bytes(str(str_input), encoding='utf-8'))
        str_input = m5.hexdigest()
        contain = True
        for f in self.hashFunc:
            loc = f.hash(str_input)
            contain = contain & self.sever.getbit(key, loc)
        return contain

    def insert(self, str_input, key=None):
        if not key:
            key = self.key
        m5 = md5()
        m5.update(bytes(str(str_input), encoding='utf-8'))
        str_input = m5.hexdigest()
        for f in self.hashFunc:
            loc = f.hash(str_input)
            self.sever.setbit(key, loc, 1)


if __name__ == '__main__':
    import time
    r = redis.StrictRedis()
    bf = MyBloomFilter(bit_size=1 << 23, db=1)
    url = 'http://www.hanhande.com/manhua/op/26129.shtml'
    print(bf.is_contains(url, key='bf_seen_urls'))
    print(bf.is_contains(url, key='bf_done_urls'))
    # start = time.time()
    # Flag = True
    # i = 0
    # while Flag:
    #
    #
    # end = time.time()
    # print('cost:{}'.format(end-start))