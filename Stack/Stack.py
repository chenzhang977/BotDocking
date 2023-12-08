import asyncio
import threading
import time
import traceback
import schedule

import Util.Log as Log
import Util.DB.DB as DB
import Util.BF2042 as BF2042
import Util.Update as Update
import Util.Message.MessageManager as MessageManager

def init_stack():
    thread = threading.Thread(target = start_task)
    thread.start()

def start_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    create_stack()
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            s = traceback.format_exc()
            Log.logger.info(e)
            Log.logger.info(s)

        time.sleep(1)

def create_stack():
    DB.init()
    # 消息队列
    schedule.every(1).seconds.do(MessageManager.send_sync_message)
    schedule.every(1).minutes.do(Update.fetch_apply_update)
    # 更新战绩
    schedule.every(1).hours.do(BF2042.update_all_info)
    # 战绩播报
    schedule.every(8).hours.do(BF2042.record_broadcast)
    #schedule.every(5).seconds.do(record_broadcast)