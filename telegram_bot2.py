#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Rapberry pi bot

from telegram.ext import Updater, CommandHandler, Job
import logging
import subprocess
import os
from functools import wraps

TOKEN = os.environ.get('BOT_TOKEN') # Bot token value
ADMIN_ID = os.environ.get('BOT_ADMIN_ID') # Only admin can send message to this bot
try:
    ADMIN_ID = int(ADMIN_ID)
except:
    pass


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)




LIST_OF_ADMINS = [ADMIN_ID, ]

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            logging.warning("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def start(bot, update):
    update.message.reply_text('Hi!')

@restricted
def ping(bot, update):
    update.message.reply_text('pong')

@restricted
def tts(bot,update):
    """Say text using festival ttl module"""
    text = update.message.text[5:]
    subprocess.Popen(["festival", "--tts", "--language", "russian"], stdin=subprocess.PIPE).communicate(text.encode('utf8'))

@restricted
def photo(bot,update):
    photo_id = update.update_id
    photo_name = '/tmp/telegram_bot_photo_%s.jpg' % photo_id
    subprocess.call('fswebcam -q -r 1280x720 %s' % photo_name, shell=True)
    if os.path.exists(photo_name): # Check if fiel exists
        update.message.reply_text("Uploading...")
        with open(photo_name, 'rb') as f:
            update.message.reply_photo(photo=f)
        try:
            os.remove(photo_name)
        except:
            logger.debug("Cannot delete tmp file {}".format(photo_name))    
        
@restricted
def video(bot, update):
    file_id = update.update_id
    duration = 10
    file_name = '/tmp/telegram_bot_video_%s.avi' % file_id
    update.message.reply_text("Starting record...")
    subprocess.call('ffmpeg  -f v4l2 -r 25 -s 1280x720  -t {duration} -i /dev/video0 {avi_file}'.format(duration=duration, avi_file=file_name), shell=True)
    if os.path.exists(file_name): # Check if file exists
        update.message.reply_text("Uploading...")
        with open(file_name, 'rb') as f:
            update.message.reply_video(video=f)
        try:
            os.remove(file_name)
        except:
            logger.debug("Cannot delete tmp file {}".format(file_name))


@restricted
def audio(bot, update):
    file_id = update.update_id
    file_name = '/tmp/telegram_bot_audio_%s.wav' % file_id
    update.message.reply_text("Starting record...")
    subprocess.call('arecord -D plughw:1 --duration=10 -f cd -vv %s' % file_name, shell=True)
    if os.path.exists(file_name): # Check if file exists
        update.message.reply_text("Uploading...")
        with open(file_name, 'rb') as f:
            update.message.reply_audio(audio=f)
        try:
            os.remove(file_name)
        except:
            logger.debug("Cannot delete tmp file {}".format(file_name))


@restricted
def temp(bot, update):
    out = subproces.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"])
    update.message.reply_text(out)

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("tts", tts))
    dp.add_handler(CommandHandler("photo", photo))
    dp.add_handler(CommandHandler("audio", audio))
    dp.add_handler(CommandHandler("video", video))
    dp.add_handler(CommandHandler("temp", temp))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()