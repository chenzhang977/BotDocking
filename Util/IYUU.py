import os
import Config.Config as Config
import Util.System as System

bat_path = Config.iyuu.bat_path
pid = -1

def start()->int:
    global pid
    pid = System.run_bat(bat_path)
    return pid

def is_run()->bool:
    global pid
    return pid != -1 and System.is_run(pid) or False

def stop()->bool:
    global pid
    ret = pid != -1 and System.kill(pid) or True
    if ret:
        pid = -1
    return ret