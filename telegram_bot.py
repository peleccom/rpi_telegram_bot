#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Rapberry pi bot

from telegram.ext import Updater, CommandHandler, Job
import logging
import subprocess
import os
from functools import wraps
import ConfigParser
import vlc



CONFIG_FILENAME = 'config.txt'

AUDIO_FILE_NAME = 'file.mp3'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

vlc_player = None



LIST_OF_ADMINS = []

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
def measure_temp(bot, update):
    out = subprocess.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"])
    update.message.reply_text(out)


@restricted
def reboot(bot, update):
    out = subprocess.call("reboot") 


@restricted
def play_audio(bot, update):
    global vlc_player
    file_name = AUDIO_FILE_NAME
    if not vlc_player:
        vlc_player=vlc.MediaPlayer(file_name)
    vlc_player.play()

@restricted
def stop_audio(bot, update):
    global vlc_player
    if vlc_player:
        vlc_player.stop() 


@restricted
def pause_audio(bot, update):
    global vlc_player
    if vlc_player:
        vlc_player.pause() 

@restricted
def resume_audio(bot, update):
    global vlc_player
    if vlc_player:
        vlc_player.play() 

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))

    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(script_dir, CONFIG_FILENAME))
    telegram_bot_token = None
    telegram_bot_admin_id = None
    telegram_bot_token = os.environ.get('BOT_TOKEN') # Bot token value
    telegram_bot_admin_id = os.environ.get('BOT_ADMIN_ID') # Only admin can send message to this bot  
    try:
        telegram_bot_token = config.get('Telegram', 'BOT_TOKEN')
    except ConfigParser.NoOptionError:
        pass
    try:
        telegram_bot_admin_id = config.get('Telegram', 'BOT_ADMIN_ID')
    except ConfigParser.NoOptionError:
        pass
    try:
        telegram_bot_admin_id = int(telegram_bot_admin_id)
    except:
        pass
    try:
        global AUDIO_FILE_NAME
        AUDIO_FILE_NAME = config.get('Player', 'AUDIO_FILE')
    except ConfigParser.NoOptionError:
        pass
    if not telegram_bot_token or not telegram_bot_admin_id:
        print("You should provide BOT_TOKEN and BOT_ADMIN_ID")
        sys.exit(1)
    updater = Updater(telegram_bot_token)
    LIST_OF_ADMINS.append(telegram_bot_admin_id)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("tts", tts))
    dp.add_handler(CommandHandler("photo", photo))
    dp.add_handler(CommandHandler("audio", audio))
    dp.add_handler(CommandHandler("video", video))
    dp.add_handler(CommandHandler("temp", measure_temp))
    dp.add_handler(CommandHandler("reboot", reboot))
    dp.add_handler(CommandHandler("play", play_audio))
    dp.add_handler(CommandHandler("stop", stop_audio))
    dp.add_handler(CommandHandler("pause", pause_audio))
    dp.add_handler(CommandHandler("resume", resume_audio))
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