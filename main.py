import Util.TG.TGBotClient as TG
import Util.QQ.QQBotClient as QQ
import Util.Message.Message as Message
from pyrogram import filters

async def func(message: Message):
    await QQ.send_msg(message.group_id, message.log_msg())

QQ.init()
QQ.add_handler(func,634091544)
QQ.run()

'''
TG.init("tg-bot")
TG.add_handler(func,filters.group)
TG.run()
'''