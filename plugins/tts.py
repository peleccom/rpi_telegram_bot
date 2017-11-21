import subprocess
import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, RegexHandler

from plugins.plugin import BasePlugin

logger = logging.getLogger(__name__)

TEXT = 'tts_text'
END = 'tts_end'


class TTSPlugin(BasePlugin):
    name = 'tts'

    def tts(self, bot, update):
        """Say text using festival ttl module"""
        text = update.message.text[5:]
        subprocess.Popen(["festival", "--tts", "--language", "russian"], stdin=subprocess.PIPE).communicate(
            text.encode('utf8'))

    def tts_text(self, bot, update):
        """Say text using festival ttl module"""
        # text = update.message.text[5:]
        # subprocess.Popen(["festival", "--tts", "--language", "russian"], stdin=subprocess.PIPE).communicate(
        #     text.encode('utf8'))
        update.message.reply_text('converting')
        return TEXT

    def tts_start(self, bot, update):
        """Say text using festival ttl module"""
        reply_keyboard = [['Done']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('start',  reply_markup=markup)
        return TEXT

    def tts_done(self, bot, update):
        """Say text using festival ttl module"""
        update.message.reply_text('done')
        return ConversationHandler.END

    def config(self, dp):
        self.add_command_handler(dp, 'tts')

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('tts_start', self.tts_start)],

            states={
                TEXT: [MessageHandler(Filters.text,
                                      self.tts_text,
                                      pass_user_data=False),
                       ]
            },

            fallbacks=[RegexHandler('^Done$', self.tts_done, pass_user_data=False)]
        )

        dp.add_handler(conv_handler)
