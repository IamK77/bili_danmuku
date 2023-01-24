import sys
import traceback
import pymysql
import re
from config import logger, conf

sys.path.append("..")

ban_msg_conf = conf['ban_msg']
conf_mysql = conf['mysql']


async def to_connect():
    try:
        return pymysql.connections.Connection(host=conf_mysql['host'],
                                              port=conf_mysql['port'],
                                              user=conf_mysql['user'],
                                              password=conf_mysql['password'],
                                              database=conf_mysql['database'])
    except pymysql:
        logger.error('MySQL连接异常')


class curd_danmu:
    @logger.catch()
    def __init__(self):
        try:
            self.db = pymysql.connect(host=conf_mysql['host'],
                                      port=conf_mysql['port'],
                                      user=conf_mysql['user'],
                                      password=conf_mysql['password'],
                                      database=conf_mysql['database'])
            self.check_table()

        except pymysql.err.OperationalError as e:
            message = e.args[1]
            logger.error(f'MySQL连接不成功, 请检查配置文件或在GitHub提出issue\n抛出的错误信息:\n{message}')
            sys.exit('程序异常终止')
        logger.success('MySQL模块导入成功')

    @logger.catch()
    def check_table(self):
        cursor = self.db.cursor()
        cursor.execute("show tables;")
        tables = [cursor.fetchall()]
        table_list = [eval(tl) for tl in re.findall('(\'.*?\')', str(tables))]
        if conf_mysql['table_name'] in table_list:
            pass
        else:
            logger.warning(f'数据库中{conf_mysql["table_name"]}表不存在')
            try:
                logger.info(f'正在新建表{conf_mysql["table_name"]}中...')
                sql = f'''
                CREATE TABLE `{conf_mysql['table_name']}` (
                `id` int(255) NOT NULL AUTO_INCREMENT,
                `uid` bigint(20) DEFAULT NULL,
                `name` varchar(255) NOT NULL,
                `event_type` enum('SUPER_CHAT_MESSAGE','INTERACT_WORD','GUARD_BUY','COMBO_SEND','SEND_GIFT','DANMU_MSG') 
                NOT NULL,
                `timestamp` int(11) NOT NULL,
                `roomid` int(11) NOT NULL,
                `roomuid` int(11) NOT NULL,
                `room_name` varchar(255) NOT NULL,
                `msg` varchar(255) DEFAULT NULL,
                `price` int(10) DEFAULT NULL,
                `medal_name` varchar(255) DEFAULT NULL,
                `medal_level` varchar(255) DEFAULT NULL,
                `num` int(11) DEFAULT NULL,
                `fleet_type` enum('舰长','提督','总督') DEFAULT NULL,
                `gift_name` varchar(50) DEFAULT NULL,
                PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                '''
                cursor.execute(sql)
                cursor.close()
                self.db.commit()
                self.db.close()
                logger.warning(f'已在MySQL中新建表{conf_mysql["table_name"]}')
            except pymysql.err as e:
                logger.error(f'建表失败, 请重试\n{e}')

    @logger.catch()
    async def sql_INSERT(self, event, table_name):
        event_attr = [item for item in event]
        event_value = ["'" + event[item] + "'" for item in event]
        attr_all = ', '.join(event_attr)
        value_all = ', '.join(event_value)
        sql = f'INSERT INTO {table_name} ({attr_all}) VALUES ({value_all})'
        try:
            self.db.ping(reconnect=True)
        except pymysql:
            traceback.print_exc()
            self.db = await to_connect()
            logger.warning("db reconnect")
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            cursor.close()
        except pymysql.err.DataError as error:
            logger.error(error)
            logger.error(sql)
        except pymysql.err.ProgrammingError as error:
            logger.error(error)
            logger.error(sql)
        except pymysql.err as e:
            logger.error(f'预期之外的错误:\n{e}')
        self.db.commit()
        self.db.close()

    @logger.catch()
    async def danmuku_insert(self, sel):
        if sel["event_type"] == 'DANMU_MSG':
            if sel["msg"] in ban_msg_conf:
                return None
            elif '打卡' in sel["msg"]:
                return None
        for i in sel:
            sel[i] = str(sel[i])
        await self.sql_INSERT(event=sel, table_name=conf_mysql['table_name'])
