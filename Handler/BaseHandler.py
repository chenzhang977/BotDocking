from Util.Message.Message import Message

class BaseHandler:
    def __init__(self):
        self.group_id = 0
        self.cmd = ""
    
    async def check_cmd(self, msg: str):
        return msg.startswith(self.cmd)

    async def handle(self, message : Message):
        pass

    async def callback(self, message : Message):
        if await self.check_cmd(message.msg):
            await self.handle(message)