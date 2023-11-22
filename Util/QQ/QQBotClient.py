import botpy
from anyio import sleep
from typing import Callable
from collections import OrderedDict
from Util.QQ.QQMessageHandler import *
from Util.Message.MessageManager import *
from botpy.message import Message as QQMessage
from datetime import datetime
import Config.Config as Config

app = None
message_callback = OrderedDict()
last_message_id = 0

class QQBotClient(botpy.Client):
    async def on_message_create(self, message: QQMessage):
        global message_callback
        if str(message.channel_id) in message_callback.keys():
            for handler in message_callback[message.channel_id]:
                await handler.callback(message)

__all__ = ["run", "add_handler", "delete_msg", "send_msg", "delete_all_self_msg"]
app = None

def get_time_stamp(time) -> int:
    timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z").timestamp()
    return int(timestamp)

def init():
    global app
    intents = botpy.Intents(guild_messages=True) 
    app = QQBotClient(intents=intents)

def run():
    global app
    app.run(appid=str(Config.qq_bot_id), token=Config.qq_bot_token)

def get_msg(message: QQMessage) -> Message:
    try:
        global last_message_id
        last_message_id = message.channel_id

        time = get_time_stamp(message.timestamp)
        message_id = message.id
        group_id = message.channel_id

        group_name = "None"
        user_id =  message.author and message.author.id or 0
        
        user_name = message.author and message.author.username or None
        text = message.content

        return create_qq_message(time, group_id, group_name,user_id, user_name, message_id, text)
    except BaseException as e:
        print(e)
        print(message)
        return create_none_message()

def add_handler(func : Callable, group_id: int = 0):
    global app, message_callback
    if group_id not in message_callback:
        message_callback[str(group_id)] = []
    message_callback[str(group_id)].append(QQMessageHandler(lambda m : func(get_msg(m))))

async def delete_msg(group_id : int, message_id : int):
    global app

async def send_msg(groupo_id : int, msg : str):
    global app
    await app.api.post_message(channel_id = groupo_id, content = msg)

async def delete_all_self_msg(group_id : int):
    global app