from .Message import *

def create_none_message():
        return Message(0, 0, "", 0, "", 0, "", MessageType.TG, -1)

def create_tg_message(time: int, group_id: int, group_name: str, user_id: int, user_name: str, msg_id: int,msg: str, auto_delete: int = -1):
        return Message(time, group_id, group_name, user_id, user_name, msg_id, msg, MessageType.TG, auto_delete)

def create_qq_message(time: int, group_id: int, group_name: str, user_id: int, user_name: str, msg_id: int,msg: str, auto_delete: int = -1):
        return Message(time, group_id, group_name, user_id, user_name, msg_id, msg, MessageType.QQ, auto_delete)