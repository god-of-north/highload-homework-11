from random import randint
from datetime import datetime
from time import sleep

import redis


class TestRedisEviction():

    def __init__(self, hostname, port) -> None:
        self.r = redis.Redis(host = hostname, port = port, db = 1)
        self.all_keys = []

    def add_key(self, key):
        ttl = 10+randint(1,10)
        self.r.set(name=key, value='DATA'*2048, ex=ttl)
        self.all_keys.append([key, 0, datetime.now().strftime("%H:%M:%S.%f"), ttl, True])

    def read_random_key(self):
        i = randint(0, len(self.all_keys)-1)
        if not self.all_keys[i][4]:
            return
        ret = self.r.get(self.all_keys[i][0])
        if ret == None:
            self.all_keys[i][4] = False
            return
        self.all_keys[i][1] = self.all_keys[i][1] + 1
        self.all_keys[i][2] = datetime.now().strftime("%H:%M:%S.%f")
        self.all_keys[i][3] = self.r.ttl(self.all_keys[i][0])

    def is_evicted(self):
        keys = self.r.keys()
        return len(keys)<len(self.all_keys)

    def show_table(self):
        keys = self.r.keys()

        print("{: >10} {: >10} {: >18} {: >7} {: >7}".format(*('KEY', 'READ COUNT', 'LAST READ', 'TTL', 'LIVE')), flush=True)
        for row in self.all_keys:
            if bytes(row[0], 'ascii') not in keys:
                row[4] = False
            print("{: >10} {: >10} {: >18} {: >7} {: >7}".format(*row), flush=True)


    def run_test(self, evicted_count):
        for i in range(1000):
            self.add_key('data'+str(i))
            sleep(0.25)
            for _ in range(5):
                self.read_random_key()
            
            if self.is_evicted():
                evicted_count -= 1
            if evicted_count == 0:
                self.show_table()
                break

def test_redis_eviction(hostname, port, title):
    print(title, flush=True)
    t = TestRedisEviction(hostname, port)
    try:
        t.run_test(3)
    except Exception as e:
        t.show_table()
        print(e)
    print('\n', flush=True)

if __name__ == '__main__':
    print('Waiting for Redis...', flush=True)
    sleep(5) # wait for Redis initialization

    test_redis_eviction('redis-volatile-lru',   6379, 'volatile-lru -> Evict using approximated LRU, only keys with an expire set.')
    test_redis_eviction('redis-allkeys-lru',    6379, 'allkeys-lru -> Evict any key using approximated LRU.')
    test_redis_eviction('redis-volatile-lfu',   6379, 'volatile-lfu -> Evict using approximated LFU, only keys with an expire set.')
    test_redis_eviction('redis-allkeys-lfu',    6379, 'allkeys-lfu -> Evict any key using approximated LFU.')
    test_redis_eviction('redis-volatile-random',6379, 'volatile-random -> Remove a random key having an expire set.')
    test_redis_eviction('redis-allkeys-random', 6379, 'allkeys-random -> Remove a random key, any key.')
    test_redis_eviction('redis-volatile-ttl',   6379, 'volatile-ttl -> Remove the key with the nearest expire time (minor TTL)')
    test_redis_eviction('redis-noeviction',     6379, 'noeviction -> Don\'t evict anything, just return an error on write operations.')

