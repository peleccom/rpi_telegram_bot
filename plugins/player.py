import subprocess
import logging

import os

import vlc
from telegram.ext import CommandHandler

from plugins.plugin import BasePlugin
from settings import Settings
from utils import restricted

logger = logging.getLogger(__name__)

settings = Settings()


class PlayerPlugin(BasePlugin):
    name = 'player'

    def play(self, bot, update):
        global vlc_player
        file_name = settings.get_value('AUDIO_FILE')
        if not vlc_player:
            vlc_player = vlc.MediaPlayer(file_name)
        vlc_player.play()

    def stop(self, bot, update):
        global vlc_player
        if vlc_player:
            vlc_player.stop()

    def pause(self, bot, update):
        global vlc_player
        if vlc_player:
            vlc_player.pause()

    def resume(self, bot, update):
        global vlc_player
        if vlc_player:
            vlc_player.play()

    def volume(self, bot, update):
        global vlc_player
        if vlc_player:
            volume_value = vlc_player.audio_get_volume()
            update.message.reply_text("Current volume {}".format(volume_value))

    def volume_up(self, bot, update):
        global vlc_player
        if vlc_player:
            volume_value = vlc_player.audio_get_volume()
            volume_value += 20
            if volume_value > 150:
                volume_value = 150
            fail = vlc_player.audio_set_volume(volume_value)
            if not fail:
                update.message.reply_text("Current volume {}".format(volume_value))

    def volume_down(self, bot, update):
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
        self.add_command_handler(dp, "play")
        self.add_command_handler(dp, "stop")
        self.add_command_handler(dp, "pause")
        self.add_command_handler(dp, "resume")
        self.add_command_handler(dp, "volume")
        self.add_command_handler(dp, "volume_up")
        self.add_command_handler(dp, "volume_down")
