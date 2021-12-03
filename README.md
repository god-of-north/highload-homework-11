# Homework #11 for Highload:Projector

Scope:
- Build master-slave redis cluster
- Try all eviction strategies
- Write a wrapper for Redis Client that implement probabilistic cache clearing 

## Installation

```
git clone https://github.com/god-of-north/highload-homework-11.git
cd highload-homework-11
docker-compose -f docker-compose.eviction.yml build
docker-compose -f docker-compose.probabalistic-cache.yml build
```

## Eviction testing

Testing strategy:
- Put data in a cycle into Redis db with random TTL
- Randomly read the data
- Wait for 3 evicted items

Run with:
```
docker-compose -f docker-compose.eviction.yml up
```

Result:
```
volatile-lru -> Evict using approximated LRU, only keys with an expire set.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         14    19:43:23.446790      16       0
     data1         17    19:43:25.553337      10       1
     data2          7    19:43:26.066185       7       1
     data3         11    19:43:26.065635      13       1
     data4          9    19:43:26.842691      14       1
     data5          4    19:43:25.810700      15       1
     data6          4    19:43:26.844003      10       1
     data7          6    19:43:24.772175      13       0
     data8          8    19:43:26.579779      12       1
     data9          3    19:43:26.843477      10       1
    data10          3    19:43:25.551444      11       0
    data11          2    19:43:25.813631      14       1
    data12          2    19:43:26.583821      11       1
    data13          2    19:43:26.067752      19       1
    data14          1    19:43:26.321692      17       1
    data15          0    19:43:25.559360      12       1
    data16          0    19:43:25.814895      20       1
    data17          2    19:43:26.585976      14       1
    data18          0    19:43:26.327363      14       1
    data19          0    19:43:26.591832      18       1


allkeys-lru -> Evict any key using approximated LRU.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         18    19:43:31.275869      15       1
     data1         18    19:43:31.274511      15       1
     data2          8    19:43:31.013513      15       1
     data3          5    19:43:29.438036      17       1
     data4          5    19:43:30.492885      10       1
     data5          7    19:43:30.753007      16       1
     data6          1    19:43:29.176664      10       0
     data7         10    19:43:31.796894       8       1
     data8          4    19:43:32.050036       8       1
     data9          1    19:43:29.700579      18       0
    data10          6    19:43:32.049094      12       1
    data11          2    19:43:31.009059      19       1
    data12          4    19:43:31.796137      14       1
    data13          0    19:43:30.236411      16       0
    data14          1    19:43:31.538944      17       1
    data15          3    19:43:31.795342      15       1
    data16          1    19:43:31.793714      16       1
    data17          2    19:43:31.534672      14       1
    data18          2    19:43:32.049463      16       1
    data19          0    19:43:31.798370      12       1


volatile-lfu -> Evict using approximated LFU, only keys with an expire set.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         18    19:43:35.987226      10       1
     data1          9    19:43:37.025306      14       1
     data2         15    19:43:37.280947       8       1
     data3          8    19:43:35.194679      17       1
     data4          9    19:43:36.507687       9       1
     data5         13    19:43:37.025726      15       1
     data6          4    19:43:36.769573       9       1
     data7          6    19:43:37.024370      10       1
     data8          3    19:43:36.765260      15       1
     data9          2    19:43:37.282205       8       1
    data10          6    19:43:36.761199       9       1
    data11          2    19:43:37.279624      17       1
    data12          1    19:43:35.985164      18       1
    data13          1    19:43:36.767366      18       1
    data14          0    19:43:35.726049      11       0
    data15          0    19:43:35.990759      18       0
    data16          0    19:43:36.255206      13       1
    data17          0    19:43:36.509149      18       0
    data18          0    19:43:36.773583      14       1
    data19          1    19:43:37.278310      18       1


allkeys-lfu -> Evict any key using approximated LFU.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         17    19:43:41.719430      12       1
     data1          8    19:43:39.886756      17       1
     data2         11    19:43:41.973900      13       1
     data3          7    19:43:40.923458       8       0
     data4          7    19:43:40.925949      15       1
     data5          8    19:43:41.455453      17       1
     data6         11    19:43:42.229835      13       1
     data7          6    19:43:42.231563      17       1
     data8          6    19:43:42.487421      11       1
     data9          3    19:43:41.446906      12       1
    data10          0    19:43:39.895655      17       1
    data11          3    19:43:40.916930      16       1
    data12          3    19:43:41.453423      16       1
    data13          0    19:43:40.664891      14       0
    data14          2    19:43:41.448916      16       1
    data15          2    19:43:41.974929      11       1
    data16          0    19:43:41.459224      18       1
    data17          2    19:43:42.486917      13       1
    data18          0    19:43:41.975870      12       0
    data19          0    19:43:42.236106      11       1


volatile-random -> Remove a random key having an expire set.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         14    19:43:45.880856       8       1
     data1         13    19:43:47.700044       9       1
     data2         10    19:43:47.180217      14       1
     data3          7    19:43:47.437940      10       1
     data4         10    19:43:46.926693      15       1
     data5          7    19:43:47.180584       8       0
     data6          7    19:43:47.442005       8       1
     data7          7    19:43:47.181230      14       1
     data8          3    19:43:47.439986       9       1
     data9          5    19:43:47.435941      12       1
    data10          7    19:43:47.703115      11       1
    data11          3    19:43:47.705065       9       1
    data12          1    19:43:46.402759      17       1
    data13          2    19:43:46.664499      18       1
    data14          1    19:43:46.927937      10       0
    data15          1    19:43:47.433893      11       0
    data16          1    19:43:46.927126      12       1
    data17          0    19:43:46.929182      13       1
    data18          0    19:43:47.181833      11       1
    data19          0    19:43:47.445737      17       1


allkeys-random -> Remove a random key, any key.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         17    19:43:52.678055      15       0
     data1         17    19:43:52.937561      10       1
     data2          9    19:43:52.414881      10       1
     data3         11    19:43:52.157209      12       1
     data4         10    19:43:51.643151      10       1
     data5          2    19:43:52.419107      17       1
     data6          8    19:43:52.675860      16       1
     data7          1    19:43:50.066601      11       1
     data8          3    19:43:52.157601      11       1
     data9          2    19:43:51.112726      13       0
    data10          5    19:43:52.941695      17       1
    data11          5    19:43:52.939548       9       1
    data12          2    19:43:52.943760      14       1
    data13          4    19:43:52.410909      18       1
    data14          1    19:43:52.156792      14       1
    data15          1    19:43:52.680114      11       1
    data16          0    19:43:51.905688      19       0
    data17          0    19:43:52.158771      11       1
    data18          0    19:43:52.422766      12       1
    data19          0    19:43:52.685725      12       1


volatile-ttl -> Remove the key with the nearest expire time (minor TTL)
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         18    19:43:56.585178      14       1
     data1         13    19:43:58.138842       7       1
     data2         14    19:43:57.356406      14       1
     data3          9    19:43:56.063106      10       0
     data4         13    19:43:57.354423       9       1
     data5          4    19:43:57.093595      15       1
     data6          3    19:43:56.839591      18       1
     data7          2    19:43:57.876564      13       1
     data8          1    19:43:55.545638      10       1
     data9          3    19:43:57.875237      15       1
    data10          4    19:43:57.878980       9       1
    data11          5    19:43:57.617818       9       0
    data12          2    19:43:57.611871      17       1
    data13          0    19:43:56.324522      19       1
    data14          0    19:43:56.588721      11       0
    data15          1    19:43:57.352418      15       1
    data16          2    19:43:57.619909      18       1
    data17          2    19:43:58.134630      19       1
    data18          1    19:43:58.140849      15       1
    data19          1    19:43:58.136722      18       1


noeviction -> Don't evict anything, just return an error on write operations.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         26    19:44:02.061482      16       1
     data1         13    19:44:02.062597       7       1
     data2          9    19:44:02.578677      12       1
     data3          4    19:44:02.577230      13       1
     data4          6    19:44:02.577605      15       1
     data5          5    19:44:01.280853      10       1
     data6          4    19:44:01.279120      18       1
     data7          2    19:44:01.280269      15       1
     data8          5    19:44:02.578321      12       1
     data9          3    19:44:02.577974      17       1
    data10          2    19:44:02.319037      15       1
    data11          0    19:44:01.027486      11       1
    data12          1    19:44:01.805758      18       1
    data13          4    19:44:02.322831      19       1
    data14          1    19:44:02.317183      16       1
    data15          0    19:44:02.063572      19       1
    data16          0    19:44:02.326513      16       1
OOM command not allowed when used memory > 'maxmemory'.
```

## Caching library

There are two ways for implemet caching using this library:
- using decorator
- using class method

Decorator case:
```
# append decorator to your function
@cache(redis, 30, 1.0)
def upper_cached(word:str):
    return word.upper()

# than call your fuction
ret = upper_cached(text)
print(ret)
```

Class method case:
```
def upper(word:str):
    return word.upper()

redis = Redis(host = 'redis', port = 6379, db = 1)
ret = redis.get_cached(text, lambda: upper(text), 30)
print(res)
```

## Redis master-slave cluster

Running container
```
docker-compose -f docker-compose.cluster.yml up
```

Slave started with
```
redis-server --slaveof redis-master 6379
```
