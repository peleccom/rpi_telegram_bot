import subprocess
import logging

import os

from telegram.ext import CommandHandler

from utils import restricted

logger = logging.getLogger(__name__)


class TTSPlugin(object):
    name = 'tts'

    def tts(self, bot, update):
        """Say text using festival ttl module"""
        text = update.message.text[5:]
        subprocess.Popen(["festival", "--tts", "--language", "russian"], stdin=subprocess.PIPE).communicate(
            text.encode('utf8'))

    def config(self, dp):
        dp.add_handler(CommandHandler("tts", restricted(self.tts)))