import asyncio
import traceback
import Util.TG.TGBotClient as TG
import Util.QQ.QQBotClient as QQ

from .Message import Message, MessageType

sync_message_queue = []

async def create_none_message():
        return Message(0, 0, "", 0, "", 0, "", MessageType.NULL, -1)

async def create_tg_message(time: int = 0, group_id: int = 0, group_name: str = "", user_id: int = 0, user_name: str = "", msg_id: int = 0, msg: str = "", auto_delete: int = -1):
        return Message(time, group_id, group_name, user_id, user_name, msg_id, msg, MessageType.TG, auto_delete)

async def create_qq_message(time: int = 0, group_id: int = 0, group_name: str = "", user_id: int = 0, user_name: str = "", msg_id: int = 0, msg: str = "", auto_delete: int = -1):
        return Message(time, group_id, group_name, user_id, user_name, msg_id, msg, MessageType.QQ, auto_delete)

async def create_message(time: int = 0, group_id: int = 0, group_name: str = "", user_id: int = 0, user_name: str = "", msg_id: int = 0, msg: str = "", auto_delete: int = -1, type: MessageType = MessageType.NULL):
        return Message(time, group_id, group_name, user_id, user_name, msg_id, msg, type, auto_delete)

def create_sync_message(time: int = 0, group_id: int = 0, group_name: str = "", user_id: int = 0, user_name: str = "", msg_id: int = 0, msg: str = "", auto_delete: int = -1, type: MessageType = MessageType.NULL):
        return Message(time, group_id, group_name, user_id, user_name, msg_id, msg, type, auto_delete)

async def send_message(message: Message):
        if message.msg_type == MessageType.NULL:
                return
        elif message.msg_type == MessageType.TG:
                await TG.send_msg(message.group_id, message.msg)
        elif message.msg_type == MessageType.QQ:
                await QQ.send_msg(message.group_id, message.msg)

def send_sync_message():
        global sync_message_queue
        loop = asyncio.get_event_loop()
        for message in sync_message_queue:
                try:
                        loop.run_until_complete(send_message(message))
                except Exception as e:
                        s = traceback.format_exc()
                        print(e)
                        print(s)
        sync_message_queue = []

def add_message(message: Message):
        global sync_message_queue
        sync_message_queue.append(message)
