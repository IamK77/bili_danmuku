from bilibili_api import live
from src import data_deal
from config import logger


@logger.catch()
async def to_use(uid):
    check = live.LiveRoom(uid)
    get = await check.get_room_info()
    owner_name = get['anchor_info']['base_info']['uname']
    roomuid = get['room_info']['uid']
    room = live.LiveDanmaku(uid)
    data_to_deal = data_deal.deal_event()

    @room.on('DANMU_MSG')
    async def on_danmuku(event):  # 收到弹幕
        await data_to_deal.center(event=event, uid=uid, roomuid=roomuid, owner_name=owner_name)

    @room.on('SEND_GIFT')
    async def on_gift(event):  # 收到礼物
        await data_to_deal.center(event=event, uid=uid, roomuid=roomuid, owner_name=owner_name)

    @room.on('COMBO_SEND')
    async def combo_gift(event):  # 收到礼物
        await data_to_deal.center(event=event, uid=uid, roomuid=roomuid, owner_name=owner_name)

    @room.on('GUARD_BUY')
    async def get_GUARD(event):  # 大航海
        await data_to_deal.center(event=event, uid=uid, roomuid=roomuid, owner_name=owner_name)

    @room.on('SUPER_CHAT_MESSAGE')
    async def get_SC(event):  # 收到SC
        await data_to_deal.center(event=event, uid=uid, roomuid=roomuid, owner_name=owner_name)

    @room.on('INTERACT_WORD')
    async def get_SC(event):  # 进入房间
        await data_to_deal.center(event=event, uid=uid, roomuid=roomuid, owner_name=owner_name)

    await room.connect()
