import subprocess
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, RegexHandler

from plugins.plugin import BasePlugin

logger = logging.getLogger(__name__)

TEXT = 'tts_text'
END = 'tts_end'


def tts_convert(text):
    try:
        subprocess.Popen(["festival", "--tts", "--language", "russian"], stdin=subprocess.PIPE).communicate(
            text.encode('utf8'))
        return True
    except Exception as e:
        logger.exception(e)
        return False


class TTSPlugin(BasePlugin):
    name = 'tts'

    def tts(self, bot, update):
        """Say text using festival ttl module"""
        text = update.message.text[5:]
        tts_convert(text)
        update.message.reply_text('done')

    def tts_text(self, bot, update):
        """Say text using festival ttl module"""
        text = update.message.text
        if tts_convert(text):
            update.message.reply_text('converted')
        return TEXT

    def tts_start(self, bot, update):
        """Say text using festival ttl module"""
        reply_keyboard = [['Done']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('start', reply_markup=markup)
        return TEXT

    def tts_done(self, bot, update):
        """Say text using festival ttl module"""
        reply_markup = ReplyKeyboardRemove()
        update.message.reply_text('done', reply_markup=reply_markup)
        return ConversationHandler.END

    def config(self, dp):
        self.names.append('tts_start')

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('tts_start', self.tts_start)],

            states={
                TEXT: [
                    RegexHandler('^Done$', self.tts_done, pass_user_data=False),
                    MessageHandler(Filters.text,
                                   self.tts_text,
                                   pass_user_data=False),
                ]
            },

            fallbacks=[RegexHandler('^Done$', self.tts_done, pass_user_data=False)]
        )

        dp.add_handler(conv_handler)
