import logging
from logging import Logger


class LogHelper(Logger):

    def __init__(self, name: str = "quants", level: str = "INFO"):
        super().__init__(name, level)
        # self.logger = logging.getLogger(name)
        self.setLevel(level)
        self.add_streamHandler()

    def add_streamHandler(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.addHandler(ch)


qlogger = LogHelper()
