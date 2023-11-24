from pyrogram import filters

import Util.TG.TGBotClient as TG
import Util.QQ.QQBotClient as QQ
import Util.Message.Message as Message

async def qq_func(message: Message):
    message.log_msg()
    await TG.send_msg(-4078426436, message.msg)

async def tg_func(message: Message):
    message.log_msg()
    if message.group_id == -4078426436 and message.user_id == 5863448060:
        await QQ.add_message(634216710, message.msg)

if __name__ == "__main__":
    QQ.init()
    QQ.add_handler(qq_func, 634216710)

    QQ.start_task()

    TG.init("tg-bot")
    TG.add_handler(tg_func, filters.group)
    TG.run()
    while True:
        pass