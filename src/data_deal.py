import time
from sql import conn_redis
from src import Timer

sql_to_conn = Timer.sql_to_conn
redis_conn = conn_redis.insert_redis()


class deal_event:

    def __init__(self):
        self.owner_name = None
        self.roomuid = None
        self.event = None
        self.uid = None

    async def center(self, event, uid, roomuid, owner_name):
        self.event = event
        self.uid = uid
        self.roomuid = roomuid
        self.owner_name = owner_name
        event_type = self.event['type']
        if event_type == 'DANMU_MSG':
            await self.DANMU_MSG()
        elif event_type == 'SEND_GIFT':
            await self.SEND_GIFT()
        elif event_type == 'COMBO_SEND':
            await self.COMBO_SEND()
        elif event_type == 'GUARD_BUY':
            await self.GUARD_BUY()
        elif event_type == 'SUPER_CHAT_MESSAGE':
            await self.SUPER_CHAT_MESSAGE()
        elif event_type == 'INTERACT_WORD':
            await self.INTERACT_WORD()

    async def DANMU_MSG(self):
        event_type = self.event['type']
        data = self.event['data']['info']
        danmu_msg = data[1]
        user_name = data[2][1]
        user_uid = data[2][0]
        medal = data[3]
        timestamp_get = data[0][4]
        timestamp = str(timestamp_get)[0:10]
        sql_dict = {"uid": user_uid, "name": user_name, "event_type": event_type,
                    "timestamp": timestamp, "roomid": self.uid, "roomuid": self.roomuid,
                    "msg": danmu_msg, "room_name": self.owner_name}
        if len(medal) != 0:
            medal_name = medal[1]
            medal_level = medal[0]
            sql_dict["medal_name"] = medal_name
            sql_dict["medal_level"] = medal_level
        await sql_to_conn.danmuku_insert(sql_dict)

    async def SEND_GIFT(self):
        event_type = self.event['type']
        data = self.event["data"]["data"]
        gift_name = data["giftName"]
        gift_num = data["num"]
        user_uid = data["uid"]
        user_name = data["uname"]
        medal = data["medal_info"]
        timestamp = data["timestamp"]
        sql_dict = {"uid": user_uid, "name": user_name, "event_type": event_type,
                    "timestamp": timestamp, "roomid": self.uid, "roomuid": self.roomuid,
                    "gift_name": gift_name, "num": gift_num, "room_name": self.owner_name}
        if medal["medal_name"]:
            medal_name = medal["medal_name"]
            medal_level = medal["medal_level"]
            sql_dict["medal_name"] = medal_name
            sql_dict["medal_level"] = medal_level
        await redis_conn.center(sql_dict)

    async def COMBO_SEND(self):
        event_type = self.event['type']
        data = self.event["data"]["data"]
        gift_name = data["gift_name"]
        gift_num = data["combo_num"]
        user_uid = data["uid"]
        user_name = data["uname"]
        timestamp = time.time()
        medal = data["medal_info"]
        sql_dict = {"uid": user_uid, "name": user_name, "event_type": event_type,
                    "timestamp": timestamp, "roomid": self.uid, "roomuid": self.roomuid,
                    "gift_name": gift_name, "num": gift_num, "room_name": self.owner_name}
        if medal["medal_name"]:
            medal_name = medal["medal_name"]
            medal_level = medal["medal_level"]
            sql_dict["medal_name"] = medal_name
            sql_dict["medal_level"] = medal_level
        await sql_to_conn.danmuku_insert(sql_dict)

    async def GUARD_BUY(self):
        event_type = self.event['type']
        data = self.event["data"]["data"]
        user_uid = data["uid"]
        user_name = data["username"]
        fleet_num = data["num"]
        fleet_price = data["price"]
        fleet_name = data["gift_name"]
        timestamp = data["start_time"]
        sql_dict = {"uid": user_uid, "name": user_name, "event_type": event_type,
                    "timestamp": timestamp, "roomid": self.uid, "roomuid": self.roomuid,
                    "price": fleet_price, "num": fleet_num, "fleet_type": fleet_name, "room_name": self.owner_name}
        await sql_to_conn.danmuku_insert(sql_dict)

    async def SUPER_CHAT_MESSAGE(self):
        event_type = self.event['type']
        data = self.event["data"]["data"]
        medal = data["medal_info"]
        user = data["user_info"]
        user_name = user["uname"]
        user_uid = data["uid"]
        sc_price = data["price"]
        timestamp = data["start_time"]
        message = data["message"]
        sql_dict = {"uid": user_uid, "name": user_name, "event_type": event_type,
                    "timestamp": timestamp, "roomid": self.uid, "roomuid": self.roomuid,
                    "msg": message, "price": sc_price, "room_name": self.owner_name}
        if medal["medal_name"]:
            medal_name = medal["medal_name"]
            medal_level = medal["medal_level"]
            sql_dict["medal_name"] = medal_name
            sql_dict["medal_level"] = medal_level
        await sql_to_conn.danmuku_insert(sql_dict)

    async def INTERACT_WORD(self):
        event_type = self.event['type']
        data = self.event["data"]["data"]
        medal = data["fans_medal"]
        timestamp = data["timestamp"]
        user_uid = data["uid"]
        user_name = data["uname"]
        sql_dict = {"uid": user_uid, "name": user_name, "event_type": event_type,
                    "timestamp": timestamp, "roomid": self.uid, "roomuid": self.roomuid,
                    "room_name": self.owner_name}
        if medal["medal_name"]:
            medal_name = medal["medal_name"]
            medal_level = medal["medal_level"]
            sql_dict["medal_name"] = medal_name
            sql_dict["medal_level"] = medal_level
        await sql_to_conn.danmuku_insert(sql_dict)
