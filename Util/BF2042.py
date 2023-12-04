import json
import traceback
import requests

from datetime import datetime, timedelta

import Util.DB.DB as DB

def get_info_by_api(name: str):
    response = requests.get('https://api.gametools.network/bf2042/stats?name=' + name)
    if response.status_code == 200:
        json_obj = json.loads(response.text)
        kill = json_obj['kills']
        deaths = json_obj['deaths']
        damage = json_obj['damage']
        if kill > 0:
            update_info(name, kill, deaths, damage)

        return {'name':name, 'kill': kill, 'deaths': deaths, 'damage': damage}
    
    return "查询异常, 请查看log"

def update_info(name: str, kill: int, deaths: int, damage: int):
    updateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cmd = f"INSERT INTO BF (updateTime, name, kill, deaths, damage) VALUES ('{updateTime}','{name}', '{kill}', '{deaths}', '{damage}')"
    try:
        DB.execute(cmd)
    except Exception as e:
        s = traceback.format_exc()
        print(e)
        print(s)

def get_record(name: str, hours: int = 24):
    end_time = datetime.now()
    start_time = end_time - timedelta(hours = hours)
    cmd = f"SELECT MAX(kill)-MIN(kill), MAX(deaths)-MIN(deaths), MAX(damage)-MIN(damage) FROM BF WHERE name='{name}' AND updateTime BETWEEN '{start_time.strftime('%Y-%m-%d %H:%M:%S')}' AND '{end_time.strftime('%Y-%m-%d %H:%M:%S')}'"
    ret = []
    try:
        ret = DB.execute(cmd)
    except Exception as e:
        s = traceback.format_exc()
        print(e)
        print(s)

    kill = 0
    deaths = 0
    damage = 0
    kd = 0
    if len(ret) == 1:
        info = ret[0]
        if len(info) == 3:
            kill = info[0] or 0
            deaths = info[1] or 0
            damage = info[2] or 0
            kd = round(kill/(deaths == 0 and 1 or deaths), 3)

    cmd = f"SELECT MAX(kill), MAX(deaths), MAX(damage) FROM BF WHERE name='{name}' AND updateTime BETWEEN '{start_time.strftime('%Y-%m-%d %H:%M:%S')}' AND '{end_time.strftime('%Y-%m-%d %H:%M:%S')}'"
    ret = []
    try:
        ret = DB.execute(cmd)
    except Exception as e:
        s = traceback.format_exc()
        print(e)
        print(s)
    
    max_kill = 0
    max_deaths = 0
    max_damage = 0
    max_kd = 0
    if len(ret) == 1:
        info = ret[0]
        if len(info) == 3:
            max_kill = info[0] or 0
            max_deaths = info[1] or 0
            max_damage = info[2] or 0
            max_kd = round(max_kill/(max_deaths == 0 and 1 or max_deaths), 3)

    return  f"name: {name}\nkill: {kill}({max_kill})\ndeaths: {deaths}({max_deaths})\ndamage: {damage}({max_damage})\nkd: {kd}({max_kd})"

def bind_id(id: int, name: str):
    cmd = f"INSERT OR REPLACE INTO user (uid, bf_name) VALUES ('{id}', '{name}')"
    return  DB.execute(cmd)

def get_name(id: int):
    cmd = f"SELECT DISTINCT bf_name FROM user WHERE uid='{id}'"
    ret = DB.execute(cmd)

    if len(ret) == 1:
        return ret[0][0]
    else:
        return None

def get_all_name():
    cmd = "SELECT DISTINCT name FROM BF"
    ret = DB.execute(cmd)
    return ret

#DB.execute("DELETE FROM BF WHERE name = 'aaa';")