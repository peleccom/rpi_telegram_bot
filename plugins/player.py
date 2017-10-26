import subprocess
import logging

import os

import vlc
from telegram.ext import CommandHandler

from settings import Settings
from utils import restricted

logger = logging.getLogger(__name__)

settings = Settings()


class PlayerPlugin(object):
    name = 'player'

    def play_audio(self, bot, update):
        global vlc_player
        file_name = settings.get_value('AUDIO_FILE')
        if not vlc_player:
            vlc_player = vlc.MediaPlayer(file_name)
        vlc_player.play()

    def stop_audio(self, bot, update):
        global vlc_player
        if vlc_player:
            vlc_player.stop()

    def pause_audio(self, bot, update):
        global vlc_player
        if vlc_player:
            vlc_player.pause()

    def resume_audio(self, bot, update):
        global vlc_player
        if vlc_player:
            vlc_player.play()

    def get_volume(self, bot, update):
        global vlc_player
        if vlc_player:
            volume_value = vlc_player.audio_get_volume()
            update.message.reply_text("Current volume {}".format(volume_value))

    def set_volume_up(self, bot, update):
        global vlc_player
        if vlc_player:
            volume_value = vlc_player.audio_get_volume()
            volume_value += 20
            if volume_value > 150:
                volume_value = 150
            fail = vlc_player.audio_set_volume(volume_value)
            if not fail:
                update.message.reply_text("Current volume {}".format(volume_value))

    def set_volume_down(self, bot, update):
        global vlc_player
        if vlc_player:
            volume_value = vlc_player.audio_get_volume()
            volume_value -= 20
            if volume_value < 0:
                volume_value = 0
            fail = vlc_player.audio_set_volume(volume_value)
            if not fail:
                update.message.reply_text("Current volume {}".format(volume_value))

    def config(self, dp):
        dp.add_handler(CommandHandler("play", restricted(self.play_audio)))
        dp.add_handler(CommandHandler("stop", restricted(self.stop_audio)))
        dp.add_handler(CommandHandler("pause", restricted(self.pause_audio)))
        dp.add_handler(CommandHandler("resume", restricted(self.resume_audio)))
        dp.add_handler(CommandHandler("volume", restricted(self.get_volume)))
        dp.add_handler(CommandHandler("volume_up", restricted(self.set_volume_up)))
        dp.add_handler(CommandHandler("volume_down", restricted(self.set_volume_down)))
