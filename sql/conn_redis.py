import sys
import redis
import time
import json
from config import logger, conf

sys.path.append("..")

set_expired_time = 15
conf_redis = conf['redis']
try:
    redis_pool = redis.ConnectionPool(host=conf_redis['host'],
                                      password=conf_redis['password'],
                                      port=conf_redis['port'],
                                      decode_responses=True)
except redis.exceptions.AuthenticationError:
    redis_pool = redis.ConnectionPool(host=conf_redis['host'],
                                      port=conf_redis['port'],
                                      decode_responses=True)
except redis:
    logger.error('redis连接不成功, 请检查配置文件或在GitHub提出issue')
    sys.exit('程序异常终止')
logger.success('redis模块导入成功')


class insert_redis:
    def __init__(self):
        self.redis_conn = redis.Redis(connection_pool=redis_pool)

    async def center(self, get_dict):
        uid = get_dict["uid"]
        uid = str(uid)
        user_list = self.redis_conn.lrange('USER_LIST', 0, -1)
        if uid in user_list:
            await self.update_gift_list(get_dict, uid)
        else:
            await self.add_gift_list(get_dict, uid)

    async def update_gift_list(self, get_dict, uid):
        expired_time = int(time.time()) + set_expired_time
        num = int(get_dict["num"])
        change_dict = json.loads(self.redis_conn.hget(name='DICT', key=uid))
        change_dict["expired_time"] = expired_time
        num_ed = int(change_dict["num"])
        change_dict["num"] = str(num_ed + num)
        print(f'新增数量' + change_dict["num"])
        change_dict = json.dumps(change_dict)
        self.redis_conn.hset(name='DICT', key=uid, value=change_dict)
        self.redis_conn.close()

    async def add_gift_list(self, get_dict, uid):
        expired_time = int(time.time()) + set_expired_time
        get_dict["expired_time"] = expired_time
        get_dict = json.dumps(get_dict)
        self.redis_conn.rpush('USER_LIST', uid)
        self.redis_conn.hset(name='DICT', key=uid, value=get_dict)
        self.redis_conn.close()
