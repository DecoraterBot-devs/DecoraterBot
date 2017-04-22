# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
from . import BotErrors


class VoiceChannel:
    """
    Class that should hopefully catch states
    for all voice channels the bot joins in on.
    """
    def __init__(self, voicechannelobj, textchannelobj):
        """
        Creates an instance of the VoiceChannel object
        to use in with the Voice Commands.

        This requires that voicechannelobj and textchannelobj
        are channel objects. This means making the objects when
        bot restarts on voice channel rejoins.

        :param voicechannelobj: Object to the Voice Channel
            the VoiceChannel object is for.
        :param textchannelobj:  Object to the Text Channel
            the VoiceChannel object is for.
        """
        self.vchannel = voicechannelobj
        self.voice_message_channel = textchannelobj
        self.voice_message_server = textchannelobj.server
        self.voice = None
        self._sent_finished_message = False
        self.is_bot_playing = False
        # to replace the temp player and normal player crap soon.
        # need to be careful to remove any done/stopped player
        # objects so it does not break the whole cog.
        # this means a lot of this cog needs rework.
        self.player_list = []
        # denotes if an error happened while joining the
        # Voice Channel.
        self.verror = False

    def add_player(self, player):
        """
        Adds an player to the Voice Channel list.

        Note: All finished / stopped players must
        be removed from the list to prevent breakage
        of this cog. To do that cache the current player
        before starting and then when it is
        finished / stopped remove it by calling
        remove_player.
        """
        # cap list at 15 players per instance.
        if len(self.player_list) < 15:
            self.player_list.append(player)
        else:
            raise BotErrors.MaxPlayersError(
                "The maximum number of players for this"
                " Voice Channel has been reached.")

    def remove_player(self, player):
        """
        Adds an player to the Voice Channel list.
        """
        self.player_list.remove(player)
