import subprocess
import logging

import os

from telegram.ext import CommandHandler

from plugins.plugin import BasePlugin
from utils import restricted

logger = logging.getLogger(__name__)


class WebCamPlugin(BasePlugin):
    name = 'webcam'

    def photo(self, bot, update):
        photo_id = update.update_id
        photo_name = '/tmp/telegram_bot_photo_%s.jpg' % photo_id
        subprocess.call('fswebcam -q -r 1280x720 %s' % photo_name, shell=True)
        if os.path.exists(photo_name):  # Check if fiel exists
            update.message.reply_text("Uploading...")
            with open(photo_name, 'rb') as f:
                update.message.reply_photo(photo=f)
            try:
                os.remove(photo_name)
            except:
                logger.debug("Cannot delete tmp file {}".format(photo_name))

    def video(self, bot, update):
        file_id = update.update_id
        duration = 10
        file_name = '/tmp/telegram_bot_video_%s.avi' % file_id
        update.message.reply_text("Starting record...")
        subprocess.call(
            'ffmpeg  -f v4l2 -r 25 -s 1280x720  -t {duration} -i /dev/video0 {avi_file}'.format(duration=duration,
                                                                                                avi_file=file_name),
            shell=True)
        if os.path.exists(file_name):  # Check if file exists
            update.message.reply_text("Uploading...")
            with open(file_name, 'rb') as f:
                update.message.reply_video(video=f)
            try:
                os.remove(file_name)
            except:
                logger.debug("Cannot delete tmp file {}".format(file_name))

    def audio(self, bot, update):
        file_id = update.update_id
        file_name = '/tmp/telegram_bot_audio_%s.wav' % file_id
        update.message.reply_text("Starting record...")
        subprocess.call('arecord -D plughw:1 --duration=10 -f cd -vv %s' % file_name, shell=True)
        if os.path.exists(file_name):  # Check if file exists
            update.message.reply_text("Uploading...")
            with open(file_name, 'rb') as f:
                update.message.reply_audio(audio=f)
            try:
                os.remove(file_name)
            except:
                logger.debug("Cannot delete tmp file {}".format(file_name))

    def config(self, dp):
        self.add_command_handler(dp, 'photo')
        self.add_command_handler(dp, 'audio')
        self.add_command_handler(dp, 'video')
