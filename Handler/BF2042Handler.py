import Util.BF2042 as BF2042
import Util.Message.MessageManager as MessageManager

from .BaseHandler import BaseHandler
from Util.Message.Message import Message

class BF2042Handler(BaseHandler):
    def __init__(self):
        self.cmd = "2042"
        self.func = {}
        self.func["24info"] = self.get_24_info
        self.func["bind"] = self.bind_id

    def help(self)->list:
        text = []
        text.append("【2042 bind name】 绑定游戏id\n")
        text.append("【2042 24info name(可选)】 可查询玩家信息,括号内为总数据,name为空时查询绑定的角色信息\n")
        return text

    async def get_game_id(self, id: int)->str:
        return  BF2042.get_name(id)

    async def get_24_info(self, id: int, name: str)->str:
        name = name == "" and await self.get_game_id(id) or name
        if not name:
            return "未绑定游戏id\n" + ''.join(self.help())
    
        BF2042.get_info_by_api(name)
        return BF2042.get_record(name)
    
    async def bind_id(self, id: int, name: str)->str:
        BF2042.bind_id(id, name)
        return await self.get_24_info(id, name)

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
