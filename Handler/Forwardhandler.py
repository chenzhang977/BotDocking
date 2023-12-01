import Config.Config as Config
import Util.Message.MessageManager as MessageManager

from .BaseHandler import BaseHandler
from Util.Message.Message import Message, MessageType

class Forwardhandler(BaseHandler):
    def __init__(self):
        self.group_id = 0
        self.cmd = ""
    
    async def handle(self, message : Message):
        if message.msg_type == MessageType.QQ:
            ret = await MessageManager.create_message(group_id = Config.tg_self_group, msg = message.msg, type = MessageType.TG)
            await MessageManager.send_message(ret)