from .BaseHandler import BaseHandler
from Util.Message.Message import Message

class LogHandler(BaseHandler):
    def __init__(self):
        self.group_id = 0
        self.cmd = ""
    
    async def handle(self, message : Message):
        message.log_msg()