import json
import os

configPath = 'Config/Config.json'

if not os.path.isfile(configPath):
    print("配置文件不存在")

with open(configPath, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

config = dict(json_data)

def __getattr__(name):
    if name in config:
        return config[name]
    else:
        return None