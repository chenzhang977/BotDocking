import time
import schedule
import multiprocessing

import Util.DB.DB as DB
import Util.BF2042 as BF2042

def init_stack():
    p = multiprocessing.Process(target = start_task)
    p.start()

def start_task():
    create_stack()
    while True:
        schedule.run_pending()
        time.sleep(1)

def create_stack():
    DB.init()
    schedule.every(1).hours.do(update_bf_info)
    #schedule.every(1).seconds.do(update_bf_info)
    
def update_bf_info():
    print("update_bf_info")
    name_list = BF2042.get_all_name()
    for name in name_list:
        print(BF2042.get_info_by_api(name[0]))