from pyrogram import filters

import Util.TG.TGBotClient as TG
import Util.QQ.QQBotClient as QQ
import Util.Message.Message as Message
import Config.Config as Config

async def qq_func(message: Message):
    message.log_msg()
    await TG.send_msg(Config.tg_self_group, message.msg)

async def tg_func(message: Message):
    message.log_msg()
    if message.group_id == Config.tg_self_group and message.user_id == Config.tg_self_id:
        await QQ.add_message(Config.qq_group_id, message.msg)

if __name__ == "__main__":
    QQ.init()
    QQ.add_handler(qq_func, Config.qq_group_id)
    QQ.add_handler(qq_func, Config.qq_test_group_id)

    QQ.start_task()

    TG.init("tg-bot")
    TG.add_handler(tg_func, filters.group)
    TG.run()
    while True:
        pass