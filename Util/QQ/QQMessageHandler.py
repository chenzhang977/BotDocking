from typing import Callable

class QQMessageHandler:
    def __init__(self, callback: Callable):
        self.callback = callback