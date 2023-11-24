import Util.TG.TGBotClient as TG
import Util.QQ.QQBotClient as QQ
import Util.Message.Message as Message
from pyrogram import filters

async def qq_func(message: Message):
    message.log_msg()
    #await QQ.send_msg(634216710, message.msg)
    #await TG.send_msg(-4078426436, message.msg)

''''''
async def tg_func(message: Message):
    message.log_msg()
    #if message.group_id == -4078426436 and message.user_id == 5863448060:
    #    #await TG.send_msg(-4078426436, message.msg)
    #await QQ.add_message(634216710, message.msg)

'''
def start_task():
    schedule.every(2).seconds.do(QQ.message_task)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_schedule_processes():
    p = Process(target = start_task)
    p.start()
'''


if __name__ == "__main__":
    QQ.init()
    QQ.add_handler(qq_func, 634216710)

    QQ.start_task()

    TG.init("tg-bot")
    TG.add_handler(tg_func, filters.group)
    TG.run()
    while True:
        pass