import json
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

        return {'kill': kill, 'deaths': deaths, 'damage': damage}

def update_info(name: str, kill: int, deaths: int, damage: int):
    updateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cmd = f"INSERT INTO BF (updateTime, name, kill, deaths, damage) VALUES ('{updateTime}','{name}', '{kill}', '{deaths}', '{damage}')"
    DB.execute(cmd)

def get_record(name: str, hours: int = 24):
    end_time = datetime.now()
    start_time = end_time - timedelta(hours = hours)
    cmd = f"SELECT MAX(kill)-MIN(kill), MAX(deaths)-MIN(deaths), MAX(damage)-MIN(damage) FROM BF WHERE name='{name}' AND updateTime BETWEEN '{start_time.strftime('%Y-%m-%d %H:%M:%S')}' AND '{end_time.strftime('%Y-%m-%d %H:%M:%S')}'"
    ret = DB.execute(cmd)

    kill = 0
    deaths = 0
    damage = 0
    if len(ret) == 1:
        info = ret[0]
        if len(info) == 3:
            kill = info[0]
            deaths = info[1]
            damage = info[2]

    return {'kill': kill, 'deaths': deaths, 'damage': damage}