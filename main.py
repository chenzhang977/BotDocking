from pyrogram import filters

import Util.Log as Log
import Util.DB.DB as DB
import Stack.Stack as Stack
import Util.Update as Update
import Util.TG.TGBotClient as TG
import Util.QQ.QQBotClient as QQ
import Handler.HandlerManager as HandlerManager


if __name__ == "__main__":
    try:
        DB.init()
        Log.logger.info(Update.check_update_info())
        Stack.init_stack()
        
        QQ.init()
        QQ.add_handler(HandlerManager.create_all_handler())

        TG.init("tg-bot")
        TG.add_handler(HandlerManager.create_all_handler(), filters.group)
        TG.run()
        
        while True:
            pass
    except Exception as e:
        Log.logger.info(e)