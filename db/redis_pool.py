import os, sys
cur_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_dir)
import redis
import logging
from db_cfg import redis_host

class BaseRedisPool(object):
    def __init__(self, host, port, password, max_connections, decode_responses, max_memory, db_select=0):
        self.db_host = host
        self.db_port = int(port)
        self.password = str(password)
        self.max_connections = max_connections
        self.decode_responses = decode_responses
        self.max_memory = max_memory
        self.db = db_select
        self.encoding = "utf-8"


class RedisClient(BaseRedisPool):
    connection_pool = None
    connection_client = None

    def __init__(self, conf_name=None):
        self.conf = mysql_host[conf_name]
        super(RedisClient, self).__init__(**self.conf)

        max_conn = 1
        if self.max_connections:
            if max_conn <= 0:
                max_conn = 1
        temp_pool = redis.ConnectionPool(host=self.db_host, port=self.db_port, db=self.db,
                                         password=self.password,
                                         encoding=self.encoding, max_connections=max_conn,
                                         decode_responses=self.decode_responses)
        self.connection_pool = temp_pool
        temp_client = redis.Redis(connection_pool=self.connection_pool)
        self.connection_client = temp_client

    # LIST COMMANDS
    def rpush(self, key, json_text, expired_in_seconds=0):
        r = self.connection_client
        pipe = r.pipeline()
        pipe.rpush(key, json_text)
        if expired_in_seconds > 0:
            pipe.expire(key, expired_in_seconds)
        pipe.execute()

    def lpush(self, key, json_text, expired_in_seconds=0):
        r = self.connection_client
        pipe = r.pipeline()
        pipe.lpush(key, json_text)
        if expired_in_seconds > 0:
            pipe.expire(key, expired_in_seconds)
        pipe.execute()

    def lpop_pipline(self, key, length):
        i = 0
        poped_items = []
        r = self.connection_client
        curent_len = r.llen(key)
        if curent_len > 0:
            target_len = 0
            if curent_len > length:
                target_len = length
            else:
                target_len = curent_len
            pipe = r.pipeline()
            while i < target_len:
                pipe.lpop(key)
                i += 1
            temp_poped_items = pipe.execute()
            poped_items = temp_poped_items
        return poped_items

    def lpop(self, key):
        poped_items = []
        r = self.connection_client
        data = r.lpop(key)
        if data:
            poped_items.append(data)
        return poped_items

    def rpop_pipline(self, key, length):
        i = 0
        poped_items = []
        r = self.connection_client

        curent_len = r.llen(key)
        if curent_len > 0:
            target_len = 0
            if curent_len > length:
                target_len = length
            else:
                target_len = curent_len
            pipe = r.pipeline()
            while i < target_len:
                pipe.rpop(key)
                i += 1
            temp_poped_items = pipe.execute()
            poped_items = temp_poped_items

        return poped_items

    def rpop(self, key):
        poped_items = []
        r = self.connection_client
        data = r.rpop(key)
        if data:
            poped_items.append(data)
        return poped_items

    def llen(self, key):
        r = self.connection_client
        result = r.llen(key)
        return result

    # HASH COMMANDS
    def hincrby(self, hash_key, field, amount=1):
        "Increment the value of ``field`` in hash ``hash_key`` by ``amount``"
        r = self.connection_client
        result = r.hincrby(hash_key, field, amount)
        return result

    def hdel(self, key, field):
        r = self.connection_client
        result = r.hdel(key, field)
        return result

    def hset(self, key, field, value, expired_in_seconds=0):
        r = self.connection_client
        pipline = r.pipeline()
        pipline.hset(key, field, value)
        if expired_in_seconds > 0:
            pipline.expire(key, expired_in_seconds)
        pipline.execute()

    def hmget(self, hash_key, fields_list):
        r = self.connection_client
        result = r.hmget(hash_key, fields_list)
        return result

    def info(self, section=None):
        r = self.connection_client

        result = r.info(section)

        return result

    def exceed_memory_limits(self):
        result = False
        if self.max_memory:

            redis_info = self.info("memory")
            distance = self.__max_memory_distance(redis_info, self.max_memory)
            if distance and distance <= 0:
                result = True
        return result

    def __max_memory_distance(self, redis_info_dict, target_max):
        # Memory
        result = None
        if "used_memory" in redis_info_dict.keys():
            temp_used = int(redis_info_dict["used_memory"])
            temp_used = temp_used / (1024 * 1024)
            result = target_max - temp_used
        else:
            logging.warning("used_memory is not found!")
        return result

    # # SET COMMANDS
    def sadd(self, key, value):
        r = self.connection_client
        result = r.sadd(key, value)
        return result

    def sismember(self, key, value):
        r = self.connection_client
        result = r.sismember(key, value)
        return result

    def scan(self, cursor, match=None, count=50):
        r = self.connection_client
        result = r.scan(cursor=cursor, match=match, count=count)
        return result

    def set(self, key, value, ex=None):
        r = self.connection_client
        result = r.set(key, value, ex)
        return result

    def get(self, key):
        r = self.connection_client
        result = r.get(key)
        return result

    def exists(self, key):
        r = self.connection_client
        result = r.exists(key)
        return result

    def keys(self, pattern):
        r = self.connection_client
        result = r.keys(pattern=pattern)
        return result

    def delele(self, key):
        r = self.connection_client
        r.delete(key)

    def close(self):
        if self.connection_pool:
            self.connection_pool.disconnect()


if __name__ == '__main__':
    redis_client = RedisClient("localRedis")
    redis_client.lpush("md", "dan")
    items = redis_client.lpop_pipline("md", 2)
    print(items)
    # print(type(items[0]))
    # print(redis_client.info())
    a = redis_client.get('')
    print(a)




