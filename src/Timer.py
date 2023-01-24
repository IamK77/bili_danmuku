import sys
import asyncio
import redis
import json
import time
from sql import conn_mysql
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sql.conn_redis import redis_pool

sys.path.append("..")
sql_to_conn = conn_mysql.curd_danmu()


sched = AsyncIOScheduler(timezone="Asia/Shanghai")


async def check():
    time_now = int(time.time())
    redis_conn = redis.Redis(connection_pool=redis_pool)
    user_list = redis_conn.lrange('USER_LIST', 0, -1)
    if len(user_list) < 1:
        pass
    else:
        for user_uid in user_list:
            user_dict = redis_conn.hget(name='DICT', key=user_uid)
            if user_dict:
                user_dict = json.loads(user_dict)
                if not user_uid:
                    print('redis_error: not found user_dict')
                else:
                    if user_dict["expired_time"] <= time_now:
                        redis_conn.hdel('DICT', user_uid)
                        redis_conn.lrem('USER_LIST', 0, user_uid)
                        user_dict.pop("expired_time")
                        await sql_to_conn.danmuku_insert(user_dict)


async def timer_check():
    while True:
        await check()
        await asyncio.sleep(3)


async def get_time(get_time_):  # 获取发送时间
    the_time = get_time_
    the_time = time.localtime(the_time)
    the_time = time.strftime("%m-%d %H:%M:%S", the_time)
    return the_time
