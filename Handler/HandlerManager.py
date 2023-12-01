from .LogHandler import LogHandler
from .HalpHandler import HalpHandler
from .BF2042Handler import BF2042Handler
from .Forwardhandler import Forwardhandler

help_text = ""

def create_all_handler():
    global help_text
    handlers = []
    handlers.append(LogHandler())
    handlers.append(HalpHandler())
    handlers.append(BF2042Handler())
    handlers.append(Forwardhandler())

    help_text = ""
    for handler in handlers:
        help_text = help_text + handler.help()

    return handlers

def get_help_text():
    return help_text