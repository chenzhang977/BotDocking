import Util.BF2042 as BF2042
import Util.Message.MessageManager as MessageManager

from .BaseHandler import BaseHandler
from Util.Message.Message import Message

class BF2042Handler(BaseHandler):
    def __init__(self):
        self.group_id = 0
        self.cmd = "2042"
        self.func = {}
        self.func["info"] = self.get_info
        self.func["24info"] = self.get_24_info
        self.func["bind"] = self.bind_id
    
    def help(self) -> str:
        text = ""
        text = text + "【2042 bind name】 绑定游戏id\n"
        text = text + "【2042 info name(可选)】 可调用api玩家信息,name为空时查询绑定的角色信息\n"
        text = text + "【2042 24info name(可选)】 可查询数据库内玩家近24小时的信息,name为空时查询绑定的角色信息\n"
        return text

    async def get_game_id(self, id: int)->str:
        return  BF2042.get_name(id)

    async def get_info(self, id: int, name:str):
        name = name == "" and await self.get_game_id(id) or name
        if not name:
            return "未绑定游戏id\n" + self.help()
        
        #改为提交任务
        return BF2042.get_info_by_api(name)

    async def get_24_info(self, id: int, name: str):
        name = name == "" and await self.get_game_id(id) or name
        if not name:
            return "未绑定游戏id\n" + self.help()
    
        return BF2042.get_record(name)
    
    async def bind_id(self, id: int, name: str):
        BF2042.bind_id(id, name)
        return await self.get_info(id, name)

    async def handle(self, message : Message):
        cmds = message.msg.split(" ")
        if len(cmds) < 2:
            return
        
        func_name = cmds[1]
        name = len(cmds) > 2 and cmds[2] or ""

        if func_name in self.func:
            msg = await self.func[func_name](message.user_id, name)
            ret = await MessageManager.create_message(group_id = message.group_id, msg = msg, type = message.msg_type)
            await MessageManager.send_message(ret)
