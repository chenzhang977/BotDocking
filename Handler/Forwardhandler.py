import Config.Config as Config
import Util.Message.MessageManager as MessageManager

from .BaseHandler import BaseHandler
from Util.Message.Message import Message, MessageType

class Forwardhandler(BaseHandler):
    def __init__(self):
        self.group_id = 0
        self.cmd = ""
    
    async def handle(self, message : Message):
        msg = f'{message.user_name}: {message.msg}' 
        if message.msg_type == MessageType.QQ:
            ret = await MessageManager.create_message(group_id = Config.tg.tg_self_group, msg = msg, type = MessageType.TG)
            await MessageManager.send_message(ret)
        if message.msg_type == MessageType.TG:
            ret = await MessageManager.create_message(group_id = Config.qq.qq_group_id, msg = msg, type = MessageType.QQ)
            MessageManager.add_message(ret)