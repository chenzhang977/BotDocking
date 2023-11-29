import traceback
import Util.Message.MessageManager as MessageManager

from pyrogram import Client
from Util.Message.Message import Message


__all__ = ["run", "add_handler", "delete_msg", "send_msg", "delete_all_self_msg"]
app = None

def get_time_stamp(time) -> int:
    return int(time.timestamp())

def init(name : str):
    global app
    app = Client(name)

def run():
    global app
    app.run()

async def get_msg(message) -> Message:
    try:
        time = get_time_stamp(message.date)
        message_id = message.id

        group_id = message.chat.id
        group_name = message.chat.title

        user_id =  message.from_user and message.from_user.id or message.sender_chat.id
        last_name = message.from_user and (message.from_user.last_name or "") or ""
        user_name = message.from_user and message.from_user.first_name + last_name or message.author_signature

        text = message.text

        return await MessageManager.create_tg_message(time, group_id, group_name,user_id, user_name, message_id, text)
    except BaseException as e:
        s = traceback.format_exc()
        print(e)
        print(s)
        return await MessageManager.create_none_message()

def add_handler(handlers, filters = None):
    global app
    @app.on_message(filters)
    async def callback(client, message):
        msg = await get_msg(message)
        for handler in handlers:
            try:
                await handler.callback(msg)
            except Exception as e:
                s = traceback.format_exc()
                print(e)
                print(s)

async def delete_msg(group_id : int, message_id : int):
    global app
    await app.delete_messages(group_id, message_id)

async def send_msg(groupo_id : int, msg : str):
    global app
    if msg == "":
        return
    
    await app.send_message(groupo_id, msg)

async def delete_all_self_msg(group_id : int):
    global app
    async for message in app.search_messages(group_id, from_user="me"):
        await delete_msg(group_id, message.id)