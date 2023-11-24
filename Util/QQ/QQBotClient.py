import time
import qqbot
import asyncio
import schedule
import threading
import multiprocessing

from datetime import datetime
from typing import Callable
from collections import OrderedDict
from qqbot.model.ws_context import WsContext
from qqbot.model.message import MessageSendRequest

import Config.Config as Config
from Util.QQ.QQMessageHandler import *
from Util.Message.MessageManager import *

APPID = Config.qq_bot_id
TOKEN = Config.qq_bot_token

message_callback = OrderedDict()
sync_messages = []

__all__ = ["init", "add_handler", "add_message", "start_task"]

def init():
    thread = threading.Thread(target = run)
    thread.start()

def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t_token = qqbot.Token(APPID, TOKEN)
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.MESSAGE_EVENT_HANDLER, message_handler)
    qqbot.async_listen_events(t_token, False, qqbot_handler)

def add_handler(func: Callable, group_id: int = 0):
    global app, message_callback
    if group_id not in message_callback:
        message_callback[str(group_id)] = []
    message_callback[str(group_id)].append(QQMessageHandler(func))

async def message_handler(context: WsContext, message: qqbot.Message):
    global message_callback
    if str(message.channel_id) in message_callback.keys():
        for handler in message_callback[message.channel_id]:
            msg_obj = await get_msg(message)
            await handler.callback(msg_obj)

async def get_time_stamp(time) -> int:
        timestamp = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z").timestamp()
        return int(timestamp)

async def get_msg(message: qqbot.Message) -> Message:
    try:
        time = await get_time_stamp(message.timestamp)
        message_id = message.id

        group_id = message.channel_id
        group_name = "None"
        user_id =  message.author and message.author.id or 0
        user_name = message.author and message.author.username or None
        text = message.content
        return await create_qq_message(time, group_id, group_name, user_id, user_name, message_id, text)
    except BaseException as e:
        print(e)
        print(message)
        return await create_none_message()  

def start_task():
    global sync_messages
    sync_messages = multiprocessing.Manager().list()
    p = multiprocessing.Process(target = start_message_task, args=(sync_messages, ))
    p.start()

def start_message_task(que):
    global sync_messages
    sync_messages = que
    schedule.every(2).seconds.do(message_task)

    while True:
        schedule.run_pending()
        time.sleep(1)

def message_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_queue_message())

async def notify_text(group_id: str, content: str):
    message_api = qqbot.AsyncMessageAPI(qqbot.Token(APPID, TOKEN), False, timeout = 6)
    await message_api.post_message(group_id, MessageSendRequest(content=content))

async def send_queue_message():
    global sync_messages
    while len(sync_messages):
        message = sync_messages.pop(0)
        try:
            await notify_text(group_id = message.group_id, content = message.msg)
        except BaseException as e:
            print(e)

async def add_message(group_id: int, content: str):
    global sync_messages
    meaasge =  await create_qq_message(int(time.time()), group_id = group_id, msg = content)
    sync_messages.append(meaasge)