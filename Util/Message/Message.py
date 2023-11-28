import datetime

class MessageType:
    NULL = 0
    TG = 1
    QQ = 2

class Message:
    def __init__(self, time: int, group_id: int, group_name: str, user_id: int, user_name: str, msg_id: int, msg: str, msg_type: MessageType, auto_delete: int = -1):
        self.time           = time
        self.group_id       = group_id
        self.group_name     = group_name
        self.user_id        = user_id
        self.user_name      = user_name
        self.msg_id         = msg_id
        self.msg            = msg
        self.msg_type       = msg_type
        self.auto_delete    = auto_delete
    
    def log_msg(self):
        datetime_obj = datetime.datetime.fromtimestamp(self.time)
        formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        text = "{}-{}({})-{}({}) : {}".format(formatted_datetime, self.group_name, self.group_id, self.user_name, self.user_id, self.msg)
        print(text)
        return text