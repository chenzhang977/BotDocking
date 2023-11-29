from .BaseHandler import BaseHandler
from Util.Message.Message import Message
import Util.BF2042 as BF2042
import Util.Message.MessageManager as MessageManager

class BF2042Handler(BaseHandler):
    def __init__(self):
        self.group_id = 0
        self.cmd = "2042"
        self.func = {}
        self.func["info"] = self.get_info
        self.func["24info"] = self.get_24_info
    
    async def get_info(self, name: str):
        info = BF2042.get_info_by_api(name)
        msg = f"kill: {info['kill']}\ndeaths: {info['deaths']}\ndamage: {info['damage']}\nkd: {info['kill']/(info['deaths'] == 0 and 1 or info['deaths'])}"
        return msg

    async def get_24_info(self, name: str):
        info = BF2042.get_record(name)
        msg = f"kill: {info['kill']}\ndeaths: {info['deaths']}\ndamage: {info['damage']}\nkd: {info['kill']/(info['deaths'] == 0 and 1 or info['deaths'])}"
        return msg
    

    async def handle(self, message : Message):
        cmds = message.msg.split(" ")
        if len(cmds) != 3:
            return
        
        func_name = cmds[1]
        name = cmds[2]

        if func_name in self.func:
            msg = await self.func[func_name](name)
            ret = await MessageManager.create_message(group_id = message.group_id, msg = msg, type = message.msg_type)
            await MessageManager.send_message(ret)
