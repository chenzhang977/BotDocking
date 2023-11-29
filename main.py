from pyrogram import filters

import Util.DB.DB as DB
import Util.TG.TGBotClient as TG
import Util.QQ.QQBotClient as QQ
import Handler.HandlerManager as HandlerManager


if __name__ == "__main__":
    DB.init()

    QQ.init()
    QQ.add_handler(HandlerManager.create_all_handler())
    QQ.start_task()

    TG.init("tg-bot")
    TG.add_handler(HandlerManager.create_all_handler(), filters.group)
    TG.run()
    
    while True:
        pass