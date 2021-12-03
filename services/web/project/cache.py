import json
from time import sleep 
from datetime import datetime
import threading
from math import log, ceil
from random import random, randint
import hashlib

import redis
import redis_lock

class Redis(redis.Redis):
    def __init__(self, *args, **kwargs):
        super(Redis, self).__init__(*args, **kwargs)

    def get_cached(self, name, func, exp, beta = 1.0):
        return cache_it(self, name, func, None, exp, beta)

def cache(conn, exp, beta):
    def func_decorator(func):
        def wrap(*args, **kwargs):
            params = (args, kwargs)
            key = hashlib.sha1( (func.__name__ + json.dumps( args + tuple(sorted(kwargs.items())))).encode('utf-8') ).hexdigest()

            result = cache_it(conn, key, func, params, exp, beta)
            
            return result
        return wrap
    return func_decorator

def cache_it(conn: redis.Redis, key, func, params, exp, beta = 1.0):
    data = conn.hgetall(key)
    if data:
        ttl = conn.ttl(key)
        computeTime = float(data[b'ct'])
        data = data[b'data']
        
        print('from cache |', key, '|', ttl, '|', computeTime, flush=True)
        
        if ceil(beta * (- log(random())) * computeTime) > ttl:
            print('>', key, 'probablistic trigger', flush=True)
            r = threading.Thread(name='recalc', target=lambda: recalc(func, params, key, exp, conn))
            r.start()

        return data
    else:
        data = recalc(func, params, key, exp, conn)
        if data:
            return data
        else:
            print('wait lock', flush=True)
            for _ in range(20):
                sleep(0.5)
                data = conn.hget(key, 'data')
                if data:
                    return json.loads(data)
            #timeout
            print('lock timeout', flush=True)
            return cache_it(conn, key, func, params, exp, beta)

def recalc(func, params, key: str, exp: int, conn: redis.Redis):
    lock = redis_lock.Lock(conn, key)
    if lock.acquire(blocking=False):
        print('from db', flush=True)
        try:
            t = datetime.now()
            if params:
                data = func(*params[0], **params[1])
            else:
                data = func()
            ct = str(ceil((datetime.now()-t).total_seconds()))

            p = conn.pipeline()
            p.hset(key, 'data', data)
            p.hset(key, 'ct', str(ct))
            p.expire(key, exp)
            p.execute()
            
            return data
        except Exception as e:
            print(e, flush=True)
        finally:
            lock.release()
    return None

if __name__ == '__main__':

    r = redis.Redis(host='localhost', port='6379', db=1)

    @cache(conn=r, exp=10, beta=1.0)
    def read_from_db(query, db):
        print(f'---reading from db simulation: {db}:{query}')
        sleep(1)
        return query

    for i in range(100):
        data = str(randint(1,9))*5
        res = read_from_db(data, 'db')
        print('@', i, ':', data, '->', res)

