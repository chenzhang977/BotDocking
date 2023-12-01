import traceback
import qqbot
import asyncio
import threading

from datetime import datetime
from Util.Message.Message import Message

import Config.Config as Config
import Util.Message.MessageManager as MessageManager

from qqbot.model.ws_context import WsContext
from qqbot.model.message import MessageSendRequest

APPID = Config.qq_bot_id
TOKEN = Config.qq_bot_token

message_handler = []

__all__ = ["init", "add_handler", "send_message"]

def init():
    thread = threading.Thread(target = run)
    thread.start()

def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t_token = qqbot.Token(APPID, TOKEN)
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.MESSAGE_EVENT_HANDLER, message_callback)
    qqbot.async_listen_events(t_token, False, qqbot_handler)

def add_handler(handler):
    global message_handler
    message_handler = handler

async def message_callback(context: WsContext, message: qqbot.Message):
    global message_callback
    msg = await get_msg(message)
    for handler in message_handler:
        try:
            await handler.callback(msg)
        except Exception as e:
            s = traceback.format_exc()
            print(e)
            print(s)

async def get_time_stamp(time) -> int:
        timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z").timestamp()
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
        return await MessageManager.create_qq_message(time, group_id, group_name, user_id, user_name, message_id, text)
    except BaseException as e:
        s = traceback.format_exc()
        print(e)
        print(s)
        return await MessageManager.create_none_message()  

async def notify_text(group_id: str, content: str):
    message_api = qqbot.AsyncMessageAPI(qqbot.Token(APPID, TOKEN), False, timeout = 6)
    await message_api.post_message(group_id, MessageSendRequest(content=content))

async def send_message(group_id: int, content: str):
    try:
        await notify_text(group_id = group_id, content = content)
    except BaseException as e:
        s = traceback.format_exc()
        print(e)
        print(s)