from .BaseHandler import BaseHandler
from Util.Message.Message import Message

import Util.IYUU as IYUU
import Util.Message.MessageManager as MessageManager

class IYUUHandler(BaseHandler):
    def __init__(self):
        self.cmd = "IYUU"
        self.func = {}
        self.func["start"] = self.start
        self.func["state"] = self.state
        self.func["stop"] = self.stop

    def help(self)->list:
        text = []
        text.append("【IYUU start】 开启IYUU\n")
        text.append("【IYUU state】 查看IYUU状态\n")
        text.append("【IYUU stop】 关闭IYUU\n")
        return text

    async def handle(self, message : Message):
        cmds = message.msg.split(" ")
        if len(cmds) < 2:
            return
        
        func_name = cmds[1]
        if func_name in self.func:
            msg = await self.func[func_name]()
            ret = await MessageManager.create_message(group_id = message.group_id, msg = msg, type = message.msg_type)
            await MessageManager.send_message(ret)

    async def start(self)->str:
        pid = IYUU.start()
        return f"IYUU已开启,进程号:{pid}"

    async def state(self)->str:
        is_run = IYUU.is_run()
        return is_run and "IYUU已开启" or "IYUU未开启"

    async def stop(self)->str:
        is_close = IYUU.stop()
        return is_close and "IYUU已关闭" or "IYUU关闭失败"