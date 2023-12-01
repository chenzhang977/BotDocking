import asyncio
import threading
import time
import schedule

import Util.DB.DB as DB
import Util.BF2042 as BF2042
import Config.Config as Config
import Util.Message.MessageManager as MessageManager
from Util.Message.Message import MessageType

def init_stack():
    thread = threading.Thread(target = start_task)
    thread.start()

def start_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    create_stack()
    while True:
        schedule.run_pending()
        time.sleep(1)

def create_stack():
    DB.init()
    # 消息队列
    schedule.every(1).seconds.do(MessageManager.send_sync_message)
    # 更新战绩
    schedule.every(1).hours.do(update_bf_info)
    # 战绩播报
    schedule.every(8).hours.do(record_broadcast)
    #schedule.every(5).seconds.do(record_broadcast)

def update_bf_info():
    name_list = BF2042.get_all_name()
    for name in name_list:
        print(BF2042.get_info_by_api(name[0]))

def record_broadcast():
    name_list = BF2042.get_all_name()
    for name in name_list:
        msg_type = MessageType.TG
        group_id = msg_type == MessageType.TG and Config.tg_self_group or Config.qq_group_id
        message = MessageManager.create_sync_message(group_id = group_id, msg = BF2042.get_record(name[0]),type = msg_type)
        MessageManager.add_message(message)