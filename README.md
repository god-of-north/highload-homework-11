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
     data0         21    13:36:56.623033      10       1
     data1         11    13:36:56.362512      12       1
     data2         16    13:36:57.405045      15       1
     data3         10    13:36:57.405917      10       1
     data4          8    13:36:56.624061       8       1
     data5          4    13:36:57.402541      16       1
     data6          3    13:36:55.051454      15       1
     data7          1    13:36:56.363442      17       1
     data8          5    13:36:55.318642      16       0
     data9          3    13:36:56.887717      13       1
    data10          4    13:36:56.106112      16       1
    data11          2    13:36:57.404177      15       1
    data12          3    13:36:56.621044      16       0
    data13          1    13:36:55.843258      12       0
    data14          1    13:36:57.145496      14       1
    data15          4    13:36:57.146025      15       1
    data16          1    13:36:56.885347      11       1
    data17          0    13:36:56.634546      11       1
    data18          1    13:36:57.403334      12       1
    data19          0    13:36:57.151451      12       1


allkeys-lru -> Evict any key using approximated LRU.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         14    13:37:00.507102       7       0
     data1         20    13:37:02.101708      15       1
     data2          8    13:37:01.311284       9       1
     data3          5    13:37:01.830832      12       1
     data4         10    13:37:00.777427      13       0
     data5          4    13:37:01.569618      15       1
     data6          8    13:37:02.650236      13       1
     data7          2    13:37:02.375693      17       1
     data8          4    13:37:02.648347      14       1
     data9          3    13:37:02.097213      15       1
    data10          1    13:37:00.244123      16       0
    data11          3    13:37:02.377907      15       1
    data12          8    13:37:02.371478      17       1
    data13          3    13:37:02.369288      13       1
    data14          3    13:37:02.646972      18       1
    data15          0    13:37:01.315311      18       1
    data16          2    13:37:02.651558      17       1
    data17          0    13:37:01.842511      13       1
    data18          0    13:37:02.116864      14       1
    data19          0    13:37:02.395380      11       1


volatile-lfu -> Evict using approximated LFU, only keys with an expire set.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         11    13:37:07.312656       6       1
     data1         13    13:37:07.569470       9       1
     data2         15    13:37:07.834198      13       1
     data3         11    13:37:07.837311      15       1
     data4          7    13:37:07.834941      12       1
     data5          2    13:37:07.572193      12       1
     data6         12    13:37:07.574230      12       1
     data7          1    13:37:06.533590      11       1
     data8          4    13:37:06.792460      14       1
     data9          5    13:37:07.050767       9       1
    data10          6    13:37:07.573279      15       1
    data11          2    13:37:06.534418      14       0
    data12          4    13:37:06.276619      17       0
    data13          1    13:37:07.570895      11       1
    data14          2    13:37:07.835694      17       1
    data15          2    13:37:07.310882      10       1
    data16          1    13:37:07.311777      19       1
    data17          0    13:37:07.058064      19       0
    data18          0    13:37:07.317974      10       1
    data19          1    13:37:07.836403      12       1


allkeys-lfu -> Evict any key using approximated LFU.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         21    13:37:12.250778      10       1
     data1          8    13:37:10.947103       7       1
     data2         14    13:37:13.038955       7       1
     data3         10    13:37:12.780415       7       1
     data4         11    13:37:13.038125      12       1
     data5          8    13:37:12.516368      16       1
     data6          8    13:37:13.038607      13       1
     data7          2    13:37:12.780845      14       1
     data8          2    13:37:13.037542      10       1
     data9          2    13:37:10.415588      11       0
    data10          4    13:37:12.518565      15       1
    data11          2    13:37:11.983914       9       1
    data12          4    13:37:12.779948      18       1
    data13          0    13:37:11.220508      18       1
    data14          1    13:37:11.986814      11       1
    data15          0    13:37:11.732816      10       0
    data16          1    13:37:12.514224      17       1
    data17          0    13:37:12.262855      11       0
    data18          0    13:37:12.529035      17       1
    data19          0    13:37:12.786820      16       1


volatile-random -> Remove a random key having an expire set.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         20    13:37:17.682545      15       1
     data1         14    13:37:18.195884       7       1
     data2         12    13:37:17.422357      15       0
     data3          7    13:37:16.905372       8       1
     data4          7    13:37:17.938032      13       1
     data5          7    13:37:17.938878       7       1
     data6          3    13:37:16.646988       7       1
     data7          7    13:37:18.196819      11       1
     data8          5    13:37:17.421516      10       1
     data9          3    13:37:17.936885      11       1
    data10          3    13:37:17.163173      15       1
    data11          3    13:37:17.937452      10       0
    data12          1    13:37:18.196337      11       1
    data13          0    13:37:16.395669      10       0
    data14          2    13:37:17.419603      12       1
    data15          0    13:37:16.911313      16       1
    data16          3    13:37:17.682202      15       1
    data17          1    13:37:18.194928      13       1
    data18          1    13:37:18.195368      17       1
    data19          0    13:37:17.944198      14       1


allkeys-random -> Remove a random key, any key.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         17    13:37:23.137806      10       1
     data1         12    13:37:21.845219      15       1
     data2          7    13:37:19.757539      10       1
     data3          9    13:37:23.137371       7       1
     data4          6    13:37:21.323873      11       0
     data5          8    13:37:23.394674      12       1
     data6          8    13:37:23.393393      16       1
     data7          7    13:37:22.364161      17       1
     data8          4    13:37:22.623027      13       1
     data9          4    13:37:23.138652      14       1
    data10          3    13:37:22.623808      16       1
    data11          3    13:37:22.622313      12       1
    data12          2    13:37:22.882771      11       1
    data13          3    13:37:22.363669      13       1
    data14          1    13:37:22.882401      17       1
    data15          1    13:37:23.138253      19       0
    data16          0    13:37:22.369163      13       0
    data17          0    13:37:22.631094      18       1
    data18          0    13:37:22.886688      17       1
    data19          0    13:37:23.142284      18       1


volatile-ttl -> Remove the key with the nearest expire time (minor TTL)
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         16    13:37:26.513329       9       0
     data1         15    13:37:28.569903      10       1
     data2          6    13:37:27.796402       7       0
     data3          9    13:37:28.572536      10       1
     data4          8    13:37:28.310966      12       1
     data5          7    13:37:28.055654      15       1
     data6          7    13:37:27.540619       9       1
     data7          9    13:37:28.310638      11       1
     data8          5    13:37:28.567213      15       1
     data9          4    13:37:28.054146       8       0
    data10          4    13:37:28.568648      16       1
    data11          3    13:37:28.310143      12       1
    data12          3    13:37:28.571213      16       1
    data13          0    13:37:26.775155      15       1
    data14          0    13:37:27.031916      13       1
    data15          1    13:37:28.311373      11       1
    data16          0    13:37:27.545459      12       1
    data17          1    13:37:28.055238      15       1
    data18          1    13:37:28.311777      10       1
    data19          0    13:37:28.315503      15       1


noeviction -> Don't evict anything, just return an error on write operations.
       KEY READ COUNT          LAST READ     TTL    LIVE
     data0         19    13:37:32.997747      16       1
     data1         12    13:37:32.999766       7       1
     data2         12    13:37:31.689152      11       1
     data3         11    13:37:32.740982      11       1
     data4          6    13:37:32.739843      14       1
     data5          4    13:37:32.999275      12       1
     data6          6    13:37:32.474571       8       1
     data7          4    13:37:32.209180      14       1
     data8          1    13:37:32.475874      13       1
     data9          1    13:37:32.470689      16       1
    data10          4    13:37:32.739175      16       1
    data11          1    13:37:32.741521      17       1
    data12          2    13:37:32.740408      11       1
    data13          0    13:37:31.956566      10       1
    data14          1    13:37:32.998267      14       1
    data15          1    13:37:32.998767      16       1
    data16          0    13:37:32.746904      15       1
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
