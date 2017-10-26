from telegram.ext import CommandHandler

from utils import restricted


class BasePlugin(object):

    def __init__(self):
        self.names = []

    def add_command_handler(self, dp, name, is_restricted=True):
        method = getattr(self, name)
        if method:
            if is_restricted:
                method = restricted(method)
            dp.add_handler(CommandHandler(name, method))
            self.names.append(name)
