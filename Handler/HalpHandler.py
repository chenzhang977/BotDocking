import Util.Message.MessageManager as MessageManager
import Handler.HandlerManager as HandlerManager

from .BaseHandler import BaseHandler
from Util.Message.Message import Message


class HalpHandler(BaseHandler):
    def __init__(self):
        self.group_id = 0
        self.cmd = "help"

    def help(self) -> str:
        text = ""
        text = text + "【help】 获取帮助信息\n"
        return text
    
    async def handle(self, message : Message):
        msg = HandlerManager.get_help_text()
        ret = await MessageManager.create_message(group_id = message.group_id, msg = msg, type = message.msg_type)
        await MessageManager.send_message(ret)