#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Rapberry pi bot
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Job, MessageHandler, Filters, Handler, StringRegexHandler, \
    RegexHandler
import logging
import subprocess
import os
from six.moves import configparser

from plugins.player import PlayerPlugin
from plugins.tts import TTSPlugin
from plugins.webcam import WebCamPlugin
from settings import Settings
import sys
from utils import restricted

CONFIG_FILENAME = 'config.txt'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

vlc_player = None

settings = Settings()

PLUGINS = [
    WebCamPlugin(),
    TTSPlugin(),
    PlayerPlugin(),
]


def start(bot, update):
    custom_keyboard = []
    for plugin in PLUGINS:
        custom_keyboard.append([plugin.name])
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text('Plugin list', reply_markup=reply_markup)


def cancel(bot, update):
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text('cancelled', reply_markup=reply_markup)


def plugin_menu_handler(bot, update):
    plugin_name = update.message.text
    selected_plugin = None
    for plugin in PLUGINS:
        if plugin.name == plugin_name:
            selected_plugin = plugin
    custom_keyboard = []
    if selected_plugin:
        for name in selected_plugin.names:
            custom_keyboard.append([name])
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(plugin_name, reply_markup=reply_markup)


@restricted
def ping(bot, update):
    update.message.reply_text('pong')


@restricted
def measure_temp(bot, update):
    out = subprocess.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"])
    update.message.reply_text(out)


@restricted
def reboot(bot, update):
    out = subprocess.call("reboot")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    list_of_admins = []

    config = configparser.RawConfigParser()
    config.read(os.path.join(script_dir, CONFIG_FILENAME))
    telegram_bot_token = None
    telegram_bot_admin_id = None
    telegram_bot_token = os.environ.get('BOT_TOKEN')  # Bot token value
    telegram_bot_admin_id = os.environ.get('BOT_ADMIN_ID')  # Only admin can send message to this bot
    try:
        telegram_bot_token = config.get('Telegram', 'BOT_TOKEN')
    except configparser.NoOptionError:
        pass
    try:
        telegram_bot_admin_id = config.get('Telegram', 'BOT_ADMIN_ID')
    except configparser.NoOptionError:
        pass
    try:
        telegram_bot_admin_id = int(telegram_bot_admin_id)
    except:
        pass
    try:
        audio_file = config.get('Player', 'AUDIO_FILE')
        settings.set_value('AUDIO_FILE', audio_file)
    except (configparser.NoOptionError, configparser.NoSectionError):
        pass
    if not telegram_bot_token or not telegram_bot_admin_id:
        print("You should provide BOT_TOKEN and BOT_ADMIN_ID")
        sys.exit(1)
    updater = Updater(telegram_bot_token)
    list_of_admins.append(telegram_bot_admin_id)
    settings.set_value('LIST_OF_ADMINS', list_of_admins)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("temp", measure_temp))
    dp.add_handler(CommandHandler("reboot", reboot))
    for plugin in PLUGINS:
        dp.add_handler(RegexHandler(plugin.name, plugin_menu_handler))
    for plugin in PLUGINS:
        plugin.config(dp)
    # log all errors
    dp.add_error_handler(error)

    print("Bot started")
    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
