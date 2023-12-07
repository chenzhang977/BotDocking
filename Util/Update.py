import os
import asyncio

from anyio import sleep

import Util.DB.DB as DB
import Util.System as System
import Config.Config as Config
import Util.Message.MessageManager as MessageManager

from Util.Message.Message import MessageType

'''
定时检查更新
有更新时运行更新脚本、结束当前进程
程序启动时判断是否更新成功(更新成功的情况下更新数据库的哈希值为本地代码的哈希值):
1、本地==云端 and 数据库==云端 无更新
2、本地==云端 and 数据库!=云端 更新成功
3、本地!=云端 and 数据库!=云端 更新失败

4、数据库无记录的情况下视为无更新,从本地获取哈希值入库并重新检查
'''
def get_local_hash()->str:
    ret = System.run_cmd("git rev-parse HEAD")
    if ret:
        hash = ret.stdout.replace("\n", "")
        return hash
    return ""

def get_git_hash()->str:
    git_url = Config.git.bot_docking_git_path
    ret = System.run_cmd(f"git ls-remote {git_url} main")
    if ret.stdout != '' and '\t' in ret.stdout:
        strs = ret.stdout.split("\t")
        return strs[0]
    print('')

def get_db_hash()->str:
    cmd = f"SELECT hash FROM git ORDER BY id DESC LIMIT 1"
    ret = DB.execute(cmd)
    if ret and len(ret) > 0:
        return ret[0][0]
    return ""

def check_update_info()->str:
    local_hash = get_local_hash()
    git_hash = get_git_hash()
    db_hash = get_db_hash()
    print("local_hash: ", local_hash)
    print("git_hash: ", git_hash)
    print("db_hash: ", db_hash)

    if db_hash == '':
        insert_hash(local_hash)
        return ''
    
    if local_hash == git_hash and git_hash == db_hash:
        return '无更新'
    elif local_hash == git_hash and git_hash != db_hash:
        insert_hash(local_hash)
        return '更新成功'
    elif local_hash != git_hash and git_hash != db_hash:
        return '更新失败, 请检查代码'
    elif local_hash != git_hash and git_hash == db_hash:
        #代码更新成功，但是更新脚本启动bot闪退，视为编译失败
        return '编译运行失败, 使用备份运行, 请检查代码'
    
def check_update()->bool:
    local_hash = get_local_hash()
    git_hash = get_git_hash()
    db_hash = get_db_hash()
    print("local_hash: ", local_hash)
    print("git_hash: ", git_hash)
    print("db_hash: ", db_hash)
    return db_hash != git_hash

async def reset_update():
    msg = '正在重启并更新'
    ret = await MessageManager.create_message(group_id = Config.tg.tg_self_group, msg = msg, type = MessageType.TG)
    await MessageManager.send_message(ret)
    #ret = MessageManager.create_sync_message(group_id = Config.qq.qq_group_id, msg = msg, type = MessageType.QQ)
    #MessageManager.add_message(ret)

    System.run_bat(f'cmd /c start cmd /c {Config.update.bat_path}', os.path.dirname(Config.update.bat_path))
    os._exit(0)

def fetch_apply_update():
    if check_update():
        asyncio.run(reset_update())

def insert_hash(hash: str):
    cmd = f"INSERT INTO git (hash) VALUES ('{hash}')"
    DB.execute(cmd)