from .LogHandler import LogHandler
from .BF2042Handler import BF2042Handler

def create_all_handler():
    handlers = []
    handlers.append(LogHandler())
    handlers.append(BF2042Handler())
    return handlers