import os
import yaml
from yaml import CLoader

configPath = 'Config/Config.yml'

if not os.path.isfile(configPath):
    print("配置文件不存在")

with open(configPath, 'r', encoding='utf-8') as f:
    data = yaml.load(f, Loader=CLoader)
    config = dict(data)

class Data:
    def __init__(self, data):
        self.data = data
    
    def __getattr__(self, name):
        if name in self.data:
            data = self.data[name]
            if type(data) == dict:
                return Data(data)
            return data
        else:
            return None

def __getattr__(name):
    if name in config:
        data = config[name]
        if type(data) == dict:
            return Data(data)
        return data
    else:
        return None