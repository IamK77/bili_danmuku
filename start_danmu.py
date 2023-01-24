from src import Timer, conn_bili
import asyncio
from config import logger, conf


@logger.catch()
async def start(uid_list):
    task = [await asyncio.to_thread(timer.timer_check)]
    logger.success('BIBL_DANMUKU正在运行')
    for i in uid_list:
        task.append(conn_bili.to_use(i))
    await asyncio.gather(*task)


if __name__ == '__main__':
    timer = Timer
    logger.success("已初始化Timer")
    asyncio.run(start(conf['room_id']))
