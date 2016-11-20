# coding=utf-8
"""
The MIT License (MIT)

Copyright (c) 2015-2016 AraHaan

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import unicode_literals
import discord
import json
import io
import sys
import os
import os.path
import youtube_dl
import ctypes
from . import BotErrors
try:
    from . import BotPMError
except ImportError:
    print('Some Unknown thing happened which made a critical bot code file unable to be found.')
    BotPMError = None
from . import BotConfigReader
from sasync import *


def dummy():
    """
    Dummy Function for __init__.py for this package on pycharm.
    :return: Nothing.
    """
    pass


class YTDLLogger(object):
    """
    Class for Silencing all of the Youtube_DL Logging stuff that defaults to console.
    """
    def __init__(self):
        self.sepa = os.sep
        self.bits = ctypes.sizeof(ctypes.c_voidp)
        self.platform = None
        if self.bits == 4:
            self.platform = 'x86'
        elif self.bits == 8:
            self.platform = 'x64'
        self.path = sys.path[0]
        self.BotConfig = BotConfigReader.BotConfigVars()
        if self.path.find('\\AppData\\Local\\Temp') != -1:
            self.path = sys.executable.strip(
                'DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(self.platform, sys.platform,
                                                                                       sys.implementation,
                                                                                       sys.version_info))
        self.PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(self.path, self.sepa)
        if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
            self.BotConfig = BotConfigReader.BotConfigVars()
            self._log_ytdl = self.BotConfig.log_ytdl

    def log_file_code(self, meth, msg):
        """
        Logs data to file (if set).
        :param meth: Method name.
        :param msg: message.
        :return: Nothing.
        """
        if meth is not '':
            if meth == 'ytdl_debug':
                logfile = '{0}{1}resources{1}Logs{1}ytdl_debug_logs.txt'.format(self.path, self.sepa)
                try:
                    file = io.open(logfile, 'a', encoding='utf-8')
                    size = os.path.getsize(logfile)
                    if size >= 32102400:
                        file.seek(0)
                        file.truncate()
                    file.write(msg + '\n')
                    file.close()
                except PermissionError:
                    return
            elif meth == 'ytdl_warning':
                logfile2 = '{0}{1}resources{1}Logs{1}ytdl_warning_logs.txt'.format(self.path, self.sepa)
                try:
                    file2 = io.open(logfile2, 'a', encoding='utf-8')
                    size = os.path.getsize(logfile2)
                    if size >= 32102400:
                        file2.seek(0)
                        file2.truncate()
                    file2.write(msg + '\n')
                    file2.close()
                except PermissionError:
                    return
            elif meth == 'ytdl_error':
                logfile3 = '{0}{1}resources{1}Logs{1}ytdl_error_logs.txt'.format(self.path, self.sepa)
                try:
                    file3 = io.open(logfile3, 'a', encoding='utf-8')
                    size = os.path.getsize(logfile3)
                    if size >= 32102400:
                        file3.seek(0)
                        file3.truncate()
                    file3.write(msg + '\n')
                    file3.close()
                except PermissionError:
                    return
            elif meth == 'ytdl_info':
                logfile4 = '{0}{1}resources{1}Logs{1}ytdl_info_logs.txt'.format(self.path, self.sepa)
                try:
                    file4 = io.open(logfile4, 'a', encoding='utf-8')
                    size = os.path.getsize(logfile4)
                    if size >= 32102400:
                        file4.seek(0)
                        file4.truncate()
                    file4.write(msg + '\n')
                    file4.close()
                except PermissionError:
                    return
        else:
            return

    def info(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if self._log_ytdl:
            self.log_file_code('ytdl_info', msg)
        else:
            pass

    def debug(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if self._log_ytdl:
            self.log_file_code('ytdl_debug', msg)
        else:
            pass

    def warning(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if self._log_ytdl:
            self.log_file_code('ytdl_warning', msg)
        else:
            pass

    def error(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if self._log_ytdl:
            self.log_file_code('ytdl_error', msg)
        else:
            pass


class BotData(BotConfigReader.BotConfigVars):
    """
        This class is for Internal use only!!!
    """
    def __init__(self):
        super(BotData, self).__init__()
        self.sepa = os.sep
        self.bits = ctypes.sizeof(ctypes.c_voidp)
        self.platform = None
        if self.bits == 4:
            self.platform = 'x86'
        elif self.bits == 8:
            self.platform = 'x64'
        self.path = sys.path[0]
        if self.path.find('\\AppData\\Local\\Temp') != -1:
            self.path = sys.executable.strip(
                'DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(self.platform, sys.platform,
                                                                                       sys.implementation,
                                                                                       sys.version_info))
        if self.bits == 4:
            if not (sys.platform.startswith('linux')):
                self.opusdll = '{0}{1}resources{1}opus{1}win32{1}{2}{1}opus.dll'.format(self.path, self.sepa,
                                                                                        self.platform)
                os.chdir('{0}{1}resources{1}ffmpeg{1}win32{1}{2}'.format(self.path, self.sepa, self.platform))
            else:
                self.opusdll = '{0}{1}resources{1}opus{1}linux{1}{2}{1}opus.dll'.format(self.path, self.sepa,
                                                                                        self.platform)
                os.chdir('{0}{1}resources{1}ffmpeg{1}linux{1}{2}'.format(self.path, self.sepa, self.platform))
        elif self.bits == 8:
            if not (sys.platform.startswith('linux')):
                self.opusdll = '{0}{1}resources{1}opus{1}win32{1}{2}{1}opus.dll'.format(self.path, self.sepa,
                                                                                        self.platform)
                os.chdir('{0}{1}resources{1}ffmpeg{1}win32{1}{2}'.format(self.path, self.sepa, self.platform))
            else:
                self.opusdll = '{0}{1}resources{1}opus{1}linux{1}{2}{1}opus.dll'.format(self.path, self.sepa,
                                                                                        self.platform)
                os.chdir('{0}{1}resources{1}ffmpeg{1}linux{1}{2}'.format(self.path, self.sepa, self.platform))
        self.botbanslist = io.open('{0}{1}resources{1}ConfigData{1}BotBanned.json'.format(self.path, self.sepa))
        self.banlist = json.load(self.botbanslist)
        self.botbanslist.close()
        try:
            self.botvoicechannelfile = io.open('{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json'.format(self.path,
                                                                                                            self.sepa))
            self.botvoicechannel = json.load(self.botvoicechannelfile)
            self.botvoicechannelfile.close()
        except FileNotFoundError:
            pass
        self.botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.{2}.json'.format(
            self.path, self.sepa, self.language))
        self.botmessages = json.load(self.botmessagesdata)
        self.botmessagesdata.close()
        self.PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(self.path, self.sepa)
        if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
            self._bot_prefix = self.bot_prefix
            self._log_ytdl = self.log_ytdl
        self.ytdlo = {'verbose': False, 'logger': YTDLLogger(), 'default_search': "ytsearch"}
        self.player = None
        self.vchannel = None
        self.vchannel_name = None
        self.voice_message_channel = None
        self.voice_message_server = None
        self.voice_message_server_name = None
        self.voice = None
        self._sent_finished_message = False
        self.sent_prune_error_message = False
        self.is_bot_playing = False
        self.bot_playlist = []
        self.bot_playlist_entries = []
        self._temp_player_1 = None
        self._temp_player_2 = None
        self._temp_player_3 = None
        self._temp_player_4 = None
        self._temp_player_5 = None
        self._temp_player_6 = None
        self._temp_player_7 = None
        self._temp_player_8 = None
        self._temp_player_9 = None
        self._temp_player_10 = None
        self.ffmop = "-nostats -loglevel quiet"
        self.verror = False
        """
        Global bool to prevent the bot from being able to join a voice channel while logging in.
        This is Essentially a fix to the bot not being able to actually send messages in the voice
        commands as they would drastically screw up.
        """
        self.lock_join_voice_channel_command = False

    def resolve_bot_playlist_issue(self):
        """
        This should fix the Memory leaks of ffmpeg processes from the temp players when a song stops playing.
        :return: Nothing.
        """
        if self.is_bot_playing is False:
            if self._temp_player_1 is not None:
                self._temp_player_1.start()
                self._temp_player_1.stop()
                self._temp_player_1 = None
            if self._temp_player_2 is not None:
                self._temp_player_2.start()
                self._temp_player_2.stop()
                self._temp_player_2 = None
            if self._temp_player_3 is not None:
                self._temp_player_3.start()
                self._temp_player_3.stop()
                self._temp_player_3 = None
            if self._temp_player_4 is not None:
                self._temp_player_4.start()
                self._temp_player_4.stop()
                self._temp_player_4 = None
            if self._temp_player_5 is not None:
                self._temp_player_5.start()
                self._temp_player_5.stop()
                self._temp_player_5 = None
            if self._temp_player_6 is not None:
                self._temp_player_6.start()
                self._temp_player_6.stop()
                self._temp_player_6 = None
            if self._temp_player_7 is not None:
                self._temp_player_7.start()
                self._temp_player_7.stop()
                self._temp_player_7 = None
            if self._temp_player_8 is not None:
                self._temp_player_8.start()
                self._temp_player_8.stop()
                self._temp_player_8 = None
            if self._temp_player_9 is not None:
                self._temp_player_9.start()
                self._temp_player_9.stop()
                self._temp_player_9 = None
            if self._temp_player_10 is not None:
                self._temp_player_10.start()
                self._temp_player_10.stop()
                self._temp_player_10 = None

    @async
    def voice_stuff_new_code(self, client, message):
        """
        Listens for the Voice Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        if message.content.startswith(self._bot_prefix + 'JoinVoiceChannel'):
            if message.author.id in self.banlist['Users']:
                return
            elif self.vchannel is not None:
                try:
                    messagedata = str(self.botmessages['join_voice_channel_command_data'][0])
                    try:
                        message_data = messagedata.format(self.voice_message_server.name)
                    except AttributeError:
                        message_data = messagedata.format(self.voice_message_server_name)
                    yield from client.send_message(message.channel, content=message_data)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)
            else:
                if not self.lock_join_voice_channel_command:
                    discord.opus.load_opus(self.opusdll)
                    self.voice_message_channel = message.channel
                    self.voice_message_server = message.channel.server
                    self.voice_message_server_name = message.channel.server.name
                    if message.author.voice_channel is not None:
                        self.vchannel = message.author.voice_channel
                        self.vchannel_name = message.author.voice_channel.name
                        if self.vchannel.id not in self.botvoicechannel:
                            self.botvoicechannel['Bot_Current_Voice_Channel'].append(self.vchannel.id)
                        if self.voice_message_server.id not in self.botvoicechannel:
                            self.botvoicechannel['Bot_Current_Voice_Channel'].append(self.voice_message_server.id)
                        if self.voice_message_channel.id not in self.botvoicechannel:
                            self.botvoicechannel['Bot_Current_Voice_Channel'].append(self.voice_message_channel.id)
                        if self.voice_message_server_name not in self.botvoicechannel:
                            self.botvoicechannel['Bot_Current_Voice_Channel'].append(self.voice_message_server_name)
                        if self.vchannel_name not in self.botvoicechannel:
                            self.botvoicechannel['Bot_Current_Voice_Channel'].append(self.vchannel_name)
                        file_name = "{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json".format(self.path, self.sepa)
                        json.dump(self.botvoicechannel, open(file_name, "w"))
                        try:
                            try:
                                self.voice = yield from client.join_voice_channel(self.vchannel)
                            except discord.errors.ConnectionClosed:
                                pass
                            except RuntimeError:
                                self.voice_message_server_name = None
                                self.vchannel_name = None
                                self.vchannel = None
                                self.voice_message_server = None
                                self.voice_message_channel = None
                                self.voice = None
                                self.verror = True
                                msgdata = str(self.botmessages['join_voice_channel_command_data'][6])
                                yield from client.send_message(self.voice_message_channel, content=msgdata)
                            if not self.verror:
                                try:
                                    msg_data = str(self.botmessages['join_voice_channel_command_data'][1]).format(
                                        self.vchannel_name)
                                    yield from client.send_message(message.channel, content=msg_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                        except discord.errors.InvalidArgument:
                            self.voice_message_channel = None
                            self.voice = None
                            self.vchannel = None
                            self.voice_message_server = None
                            self.voice_message_server_name = None
                            self.vchannel_name = None
                            try:
                                msg_data = str(self.botmessages['join_voice_channel_command_data'][2])
                                yield from client.send_message(message.channel, content=msg_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                        except asyncio.TimeoutError:
                            self.voice_message_channel = None
                            self.voice = None
                            self.vchannel = None
                            self.voice_message_server = None
                            self.voice_message_server_name = None
                            self.vchannel_name = None
                            try:
                                msg_data = str(self.botmessages['join_voice_channel_command_data'][3])
                                yield from client.send_message(message.channel, content=msg_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                        except discord.errors.ClientException:
                            self.voice_message_channel = None
                            self.voice = None
                            self.vchannel = None
                            self.voice_message_server = None
                            try:
                                msg_data = str(self.botmessages['join_voice_channel_command_data'][4])
                                yield from client.send_message(message.channel, content=msg_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                        except discord.opus.OpusNotLoaded:
                            self.voice_message_channel = None
                            self.voice = None
                            self.vchannel = None
                            self.voice_message_server = None
                            self.voice_message_server_name = None
                            self.vchannel_name = None
                            try:
                                msg_data = str(self.botmessages['join_voice_channel_command_data'][5])
                                yield from client.send_message(message.channel, content=msg_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                        except IndexError:
                            return
        if message.content.startswith(self._bot_prefix + 'play'):
            if message.author.id in self.banlist['Users']:
                return
            elif self.is_bot_playing is False:
                if self.voice is not None:
                    if self.voice_message_channel is not None:
                        if message.channel.id == self.voice_message_channel.id:
                            try:
                                data = message.content[len(self._bot_prefix + "play "):].strip()
                                if data == "":
                                    try:
                                        message_data = str(self.botmessages['play_command_data'][0])
                                        yield from client.send_message(self.voice_message_channel, content=message_data)
                                    except discord.errors.Forbidden:
                                        yield from BotPMError.resolve_send_message_error(client, message)
                                if data.rfind('https://') == -1 and data.rfind('http://') == -1:
                                    # lets try to do a search.
                                    self.player = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                                    self._sent_finished_message = False
                                    self.is_bot_playing = True
                                    if self.player is not None:
                                        try:
                                            fulldir = self.player.duration
                                            minutes = str(int((fulldir / 60) % 60))
                                            seconds = str(int(fulldir % 60))
                                            if len(seconds) == 1:
                                                seconds = "0" + seconds
                                            try:
                                                message_data = str(self.botmessages['play_command_data'][1]).format(
                                                    str(self.player.title), str(self.player.uploader), minutes, seconds)
                                                yield from client.send_message(self.voice_message_channel,
                                                                               content=message_data)
                                            except discord.errors.Forbidden:
                                                yield from BotPMError.resolve_send_message_error(client, message)
                                            try:
                                                self.player.start()
                                            except RuntimeError:
                                                pass
                                        except AttributeError:
                                            message_data = str(self.botmessages['play_command_data'][2])
                                            self.is_bot_playing = False
                                            yield from client.send_message(self.voice_message_channel,
                                                                           content=message_data)
                                else:
                                    if '<' and '>' in data:
                                        data = data.strip('<')
                                        data = data.strip('>')
                                    if 'www.youtube.com/watch?v=' in data or 'soundcloud.com' in data:
                                        self.player = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                        self._sent_finished_message = False
                                        self.is_bot_playing = True
                                        if self.player is not None:
                                            try:
                                                fulldir = self.player.duration
                                                minutes = str(int((fulldir / 60) % 60))
                                                seconds = str(int(fulldir % 60))
                                                if len(seconds) == 1:
                                                    seconds = "0" + seconds
                                                try:
                                                    message_data = str(self.botmessages['play_command_data'][1]).format(
                                                        str(self.player.title), str(self.player.uploader), minutes,
                                                        seconds)
                                                    yield from client.send_message(self.voice_message_channel,
                                                                                   content=message_data)
                                                except discord.errors.Forbidden:
                                                    yield from BotPMError.resolve_send_message_error(client, message)
                                                try:
                                                    self.player.start()
                                                except RuntimeError:
                                                    pass
                                            except AttributeError:
                                                message_data = str(self.botmessages['play_command_data'][2])
                                                self.is_bot_playing = False
                                                yield from client.send_message(self.voice_message_channel,
                                                                               content=message_data)
                            except IndexError:
                                return
                            except discord.errors.ClientException:
                                message_data = str(self.botmessages['play_command_data'][4]).format(str(sys.path))
                                yield from client.send_message(message.channel, content=message_data)
                                self.player = None
                            except youtube_dl.utils.UnsupportedError:
                                yield from client.send_message(message.channel,
                                                               content=str(self.botmessages['play_command_data'][5]))
                                self.player = None
                            except youtube_dl.utils.ExtractorError:
                                message_data = str(self.botmessages['play_command_data'][6])
                                yield from client.send_message(message.channel, content=message_data)
                                self.player = None
                            except youtube_dl.utils.DownloadError:
                                yield from client.send_message(message.channel,
                                                               content=str(self.botmessages['play_command_data'][7]))
                                self.player = None
                        else:
                            return
                else:
                    message_data = str(self.botmessages['play_command_data'][8])
                    yield from client.send_message(message.channel, content=message_data)
            else:
                if self.player is not None:
                    data = message.content[len(self._bot_prefix + "play "):].strip()
                    if data == "":
                        try:
                            message_data = str(self.botmessages['play_command_data'][9])
                            yield from client.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    else:
                        if '<' and '>' in data:
                            data = data.replace('<', '').replace('>', '')
                        if data.rfind('https://') == -1 and data.rfind('http://') == -1:
                            if len(self.bot_playlist) == 0:
                                self._temp_player_1 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist01 = self._temp_player_1.title
                                    playlist01time = self._temp_player_1.duration
                                    track1 = str(self.botmessages['play_command_data'][10]).format(playlist01)
                                    fulldir = playlist01time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track1time = newdir
                                    track1uploader = str(self._temp_player_1.uploader)
                                    track1info = str(self.botmessages['play_command_data'][12]).format(track1,
                                                                                                       track1uploader,
                                                                                                       track1time)
                                    self.bot_playlist_entries.append(track1info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track1, track1time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif data in self.bot_playlist:
                                msgdata = str(self.botmessages['play_command_data'][14])
                                message_data = msgdata
                                yield from client.send_message(message.channel, content=message_data)
                            elif len(self.bot_playlist) == 1:
                                self._temp_player_2 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist02 = self._temp_player_2.title
                                    playlist02time = self._temp_player_2.duration
                                    track2 = str(self.botmessages['play_command_data'][10]).format(playlist02)
                                    fulldir = playlist02time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track2time = newdir
                                    track2uploader = str(self._temp_player_2.uploader)
                                    track2info = str(self.botmessages['play_command_data'][12]).format(track2,
                                                                                                       track2uploader,
                                                                                                       track2time)
                                    self.bot_playlist_entries.append(track2info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track2, track2time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 2:
                                self._temp_player_3 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist03 = self._temp_player_3.title
                                    playlist03time = self._temp_player_3.duration
                                    track3 = str(self.botmessages['play_command_data'][10]).format(playlist03)
                                    fulldir = playlist03time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track3time = newdir
                                    track3uploader = str(self._temp_player_3.uploader)
                                    track3info = str(self.botmessages['play_command_data'][12]).format(track3,
                                                                                                       track3uploader,
                                                                                                       track3time)
                                    self.bot_playlist_entries.append(track3info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track3, track3time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 3:
                                self._temp_player_4 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist04 = self._temp_player_4.title
                                    playlist04time = self._temp_player_4.duration
                                    track4 = str(self.botmessages['play_command_data'][10]).format(playlist04)
                                    fulldir = playlist04time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track4time = newdir
                                    track4uploader = str(self._temp_player_4.uploader)
                                    track4info = str(self.botmessages['play_command_data'][12]).format(track4,
                                                                                                       track4uploader,
                                                                                                       track4time)
                                    self.bot_playlist_entries.append(track4info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track4, track4time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 4:
                                self._temp_player_5 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist05 = self._temp_player_5.title
                                    playlist05time = self._temp_player_5.duration
                                    track5 = str(self.botmessages['play_command_data'][10]).format(playlist05)
                                    fulldir = playlist05time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track5time = newdir
                                    track5uploader = str(self._temp_player_5.uploader)
                                    track5info = str(self.botmessages['play_command_data'][12]).format(track5,
                                                                                                       track5uploader,
                                                                                                       track5time)
                                    self.bot_playlist_entries.append(track5info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track5, track5time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 5:
                                self._temp_player_6 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist06 = self._temp_player_6.title
                                    playlist06time = self._temp_player_6.duration
                                    track6 = str(self.botmessages['play_command_data'][10]).format(playlist06)
                                    fulldir = playlist06time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track6time = newdir
                                    track6uploader = str(self._temp_player_6.uploader)
                                    track6info = str(self.botmessages['play_command_data'][12]).format(track6,
                                                                                                       track6uploader,
                                                                                                       track6time)
                                    self.bot_playlist_entries.append(track6info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track6, track6time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 6:
                                self._temp_player_7 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist07 = self._temp_player_7.title
                                    playlist07time = self._temp_player_7.duration
                                    track7 = str(self.botmessages['play_command_data'][10]).format(playlist07)
                                    fulldir = playlist07time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track7time = newdir
                                    track7uploader = str(self._temp_player_7.uploader)
                                    track7info = str(self.botmessages['play_command_data'][12]).format(track7,
                                                                                                       track7uploader,
                                                                                                       track7time)
                                    self.bot_playlist_entries.append(track7info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track7, track7time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 7:
                                self._temp_player_8 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist08 = self._temp_player_8.title
                                    playlist08time = self._temp_player_8.duration
                                    track8 = str(self.botmessages['play_command_data'][10]).format(playlist08)
                                    fulldir = playlist08time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track8time = newdir
                                    track8uploader = str(self._temp_player_8.uploader)
                                    track8info = str(self.botmessages['play_command_data'][12]).format(track8,
                                                                                                       track8uploader,
                                                                                                       track8time)
                                    self.bot_playlist_entries.append(track8info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track8, track8time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 8:
                                self._temp_player_9 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist09 = self._temp_player_9.title
                                    playlist09time = self._temp_player_9.duration
                                    track9 = str(self.botmessages['play_command_data'][10]).format(playlist09)
                                    fulldir = playlist09time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track9time = newdir
                                    track9uploader = str(self._temp_player_9.uploader)
                                    track9info = str(self.botmessages['play_command_data'][12]).format(track9,
                                                                                                       track9uploader,
                                                                                                       track9time)
                                    self.bot_playlist_entries.append(track9info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track9, track9time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 9:
                                self._temp_player_10 = yield from self.voice.create_ytdl_player(data,
                                                                                                ytdl_options=self.ytdlo,
                                                                                                options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist10 = self._temp_player_10.title
                                    playlist10time = self._temp_player_10.duration
                                    track10 = str(self.botmessages['play_command_data'][10]).format(playlist10)
                                    fulldir = playlist10time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track10time = newdir
                                    track10uploader = str(self._temp_player_10.uploader)
                                    track10info = str(self.botmessages['play_command_data'][12]).format(track10,
                                                                                                        track10uploader,
                                                                                                        track10time)
                                    self.bot_playlist_entries.append(track10info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track10,
                                                                                                    track10time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 10:
                                msgdata = str(self.botmessages['play_command_data'][15])
                                message_data = msgdata
                                yield from client.send_message(message.channel, content=message_data)
                        if 'www.youtube.com/watch?v=' in data or 'soundcloud.com' in data:
                            if len(self.bot_playlist) == 0:
                                self._temp_player_1 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist01 = self._temp_player_1.title
                                    playlist01time = self._temp_player_1.duration
                                    track1 = str(self.botmessages['play_command_data'][10]).format(playlist01)
                                    fulldir = playlist01time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track1time = newdir
                                    track1uploader = str(self._temp_player_1.uploader)
                                    track1info = str(self.botmessages['play_command_data'][12]).format(track1,
                                                                                                       track1uploader,
                                                                                                       track1time)
                                    self.bot_playlist_entries.append(track1info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track1, track1time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif data in self.bot_playlist:
                                msgdata = str(self.botmessages['play_command_data'][14])
                                message_data = msgdata
                                yield from client.send_message(message.channel, content=message_data)
                            elif len(self.bot_playlist) == 1:
                                self._temp_player_2 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist02 = self._temp_player_2.title
                                    playlist02time = self._temp_player_2.duration
                                    track2 = str(self.botmessages['play_command_data'][10]).format(playlist02)
                                    fulldir = playlist02time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track2time = newdir
                                    track2uploader = str(self._temp_player_2.uploader)
                                    track2info = str(self.botmessages['play_command_data'][12]).format(track2,
                                                                                                       track2uploader,
                                                                                                       track2time)
                                    self.bot_playlist_entries.append(track2info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track2, track2time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 2:
                                self._temp_player_3 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist03 = self._temp_player_3.title
                                    playlist03time = self._temp_player_3.duration
                                    track3 = str(self.botmessages['play_command_data'][10]).format(playlist03)
                                    fulldir = playlist03time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track3time = newdir
                                    track3uploader = str(self._temp_player_3.uploader)
                                    track3info = str(self.botmessages['play_command_data'][12]).format(track3,
                                                                                                       track3uploader,
                                                                                                       track3time)
                                    self.bot_playlist_entries.append(track3info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track3, track3time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 3:
                                self._temp_player_4 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist04 = self._temp_player_4.title
                                    playlist04time = self._temp_player_4.duration
                                    track4 = str(self.botmessages['play_command_data'][10]).format(playlist04)
                                    fulldir = playlist04time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track4time = newdir
                                    track4uploader = str(self._temp_player_4.uploader)
                                    track4info = str(self.botmessages['play_command_data'][12]).format(track4,
                                                                                                       track4uploader,
                                                                                                       track4time)
                                    self.bot_playlist_entries.append(track4info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track4, track4time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 4:
                                self._temp_player_5 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist05 = self._temp_player_5.title
                                    playlist05time = self._temp_player_5.duration
                                    track5 = str(self.botmessages['play_command_data'][10]).format(playlist05)
                                    fulldir = playlist05time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track5time = newdir
                                    track5uploader = str(self._temp_player_5.uploader)
                                    track5info = str(self.botmessages['play_command_data'][12]).format(track5,
                                                                                                       track5uploader,
                                                                                                       track5time)
                                    self.bot_playlist_entries.append(track5info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track5, track5time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 5:
                                self._temp_player_6 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist06 = self._temp_player_6.title
                                    playlist06time = self._temp_player_6.duration
                                    track6 = str(self.botmessages['play_command_data'][10]).format(playlist06)
                                    fulldir = playlist06time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track6time = newdir
                                    track6uploader = str(self._temp_player_6.uploader)
                                    track6info = str(self.botmessages['play_command_data'][12]).format(track6,
                                                                                                       track6uploader,
                                                                                                       track6time)
                                    self.bot_playlist_entries.append(track6info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track6, track6time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 6:
                                self._temp_player_7 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist07 = self._temp_player_7.title
                                    playlist07time = self._temp_player_7.duration
                                    track7 = str(self.botmessages['play_command_data'][10]).format(playlist07)
                                    fulldir = playlist07time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track7time = newdir
                                    track7uploader = str(self._temp_player_7.uploader)
                                    track7info = str(self.botmessages['play_command_data'][12]).format(track7,
                                                                                                       track7uploader,
                                                                                                       track7time)
                                    self.bot_playlist_entries.append(track7info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track7, track7time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 7:
                                self._temp_player_8 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist08 = self._temp_player_8.title
                                    playlist08time = self._temp_player_8.duration
                                    track8 = str(self.botmessages['play_command_data'][10]).format(playlist08)
                                    fulldir = playlist08time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track8time = newdir
                                    track8uploader = str(self._temp_player_8.uploader)
                                    track8info = str(self.botmessages['play_command_data'][12]).format(track8,
                                                                                                       track8uploader,
                                                                                                       track8time)
                                    self.bot_playlist_entries.append(track8info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track8, track8time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 8:
                                self._temp_player_9 = yield from self.voice.create_ytdl_player(data,
                                                                                               ytdl_options=self.ytdlo,
                                                                                               options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist09 = self._temp_player_9.title
                                    playlist09time = self._temp_player_9.duration
                                    track9 = str(self.botmessages['play_command_data'][10]).format(playlist09)
                                    fulldir = playlist09time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track9time = newdir
                                    track9uploader = str(self._temp_player_9.uploader)
                                    track9info = str(self.botmessages['play_command_data'][12]).format(track9,
                                                                                                       track9uploader,
                                                                                                       track9time)
                                    self.bot_playlist_entries.append(track9info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track9, track9time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 9:
                                self._temp_player_10 = yield from self.voice.create_ytdl_player(data,
                                                                                                ytdl_options=self.ytdlo,
                                                                                                options=self.ffmop)
                                self.bot_playlist.append(data)
                                try:
                                    playlist10 = self._temp_player_10.title
                                    playlist10time = self._temp_player_10.duration
                                    track10 = str(self.botmessages['play_command_data'][10]).format(playlist10)
                                    fulldir = playlist10time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(self.botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track10time = newdir
                                    track10uploader = str(self._temp_player_10.uploader)
                                    track10info = str(self.botmessages['play_command_data'][12]).format(track10,
                                                                                                        track10uploader,
                                                                                                        track10time)
                                    self.bot_playlist_entries.append(track10info)
                                    msgdata = str(self.botmessages['play_command_data'][13]).format(track10,
                                                                                                    track10time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, content=message_data)
                                except AttributeError:
                                    message_data = str(self.botmessages['play_command_data'][2])
                                    yield from client.send_message(self.voice_message_channel, content=message_data)
                            elif len(self.bot_playlist) == 10:
                                msgdata = str(self.botmessages['play_command_data'][15])
                                message_data = msgdata
                                yield from client.send_message(message.channel, content=message_data)
        if message.content.startswith(self._bot_prefix + 'stop'):
            if message.author.id in self.banlist['Users']:
                return
            elif self.voice_message_channel is not None:
                if message.channel.id == self.voice_message_channel.id:
                    if self.player is not None:
                        fulldir = self.player.duration
                        minutes = str(int((fulldir / 60) % 60))
                        seconds = str(int(fulldir % 60))
                        if len(seconds) == 1:
                            seconds = "0" + seconds
                        try:
                            message_data = str(self.botmessages['stop_command_data'][0]).format(str(self.player.title),
                                                                                                str(self.player.uploader
                                                                                                    ), minutes, seconds)
                            yield from client.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                        self.player.stop()
                        self.player = None
                        self.is_bot_playing = False
                        # Clean the temp players now...
                        self.resolve_bot_playlist_issue()
                        if len(self.bot_playlist) >= 1:
                            try:
                                track_data = None
                                try:
                                    track_data = str(self.bot_playlist_entries[0])
                                except IndexError:
                                    pass
                                data = str(self.bot_playlist[0])
                                self.player = yield from self.voice.create_ytdl_player(data, ytdl_options=self.ytdlo,
                                                                                       options=self.ffmop)
                                if self.player is not None:
                                    self._sent_finished_message = False
                                    try:
                                        self.bot_playlist.remove(data)
                                        self.bot_playlist_entries.remove(track_data)
                                    except ValueError:
                                        pass
                                    if self.is_bot_playing is False:
                                        self.is_bot_playing = True
                                        try:
                                            fulldir = self.player.duration
                                            minutes = str(int((fulldir / 60) % 60))
                                            seconds = str(int(fulldir % 60))
                                            if len(seconds) == 1:
                                                seconds = "0" + seconds
                                            track_info = str(self.botmessages['stop_command_data'][1]).format(
                                                str(self.player.title),
                                                str(self.player.uploader))
                                            message_data = str(self.botmessages['stop_command_data'][2]).format(
                                                track_info, minutes, seconds)
                                            yield from client.send_message(self.voice_message_channel,
                                                                           content=message_data)
                                            try:
                                                self.bot_playlist_entries.remove(track_info)
                                            except ValueError:
                                                pass
                                        except discord.errors.Forbidden:
                                            yield from BotPMError.resolve_send_message_error(client, message)
                                        if self.player is not None:
                                            self.player.start()
                            except UnboundLocalError:
                                self.player = None
                                self.is_bot_playing = False
                    else:
                        try:
                            message_data = str(self.botmessages['stop_command_data'][3])
                            yield from client.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    return
        if message.content.startswith(self._bot_prefix + 'pause'):
            if message.author.id in self.banlist['Users']:
                return
            elif self.voice_message_channel is not None:
                if message.channel.id == self.voice_message_channel.id:
                    if self.player is not None:
                        fulldir = self.player.duration
                        minutes = str(int((fulldir / 60) % 60))
                        seconds = str(int(fulldir % 60))
                        if len(seconds) == 1:
                            seconds = "0" + seconds
                        try:
                            message_data = str(self.botmessages['pause_command_data'][0]).format(
                                str(self.player.title), str(self.player.uploader), minutes, seconds)
                            yield from client.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                        self.player.pause()
                    else:
                        message_data = str(self.botmessages['pause_command_data'][1])
                        yield from client.send_message(self.voice_message_channel, content=message_data)
                else:
                    return
            else:
                message_data = str(self.botmessages['pause_command_data'][2])
                yield from client.send_message(message.channel, content=message_data)
        if message.content.startswith(self._bot_prefix + 'unpause'):
            if message.author.id in self.banlist['Users']:
                return
            elif self.voice_message_channel is not None:
                if message.channel.id == self.voice_message_channel.id:
                    if self.player is not None:
                        fulldir = self.player.duration
                        minutes = str(int((fulldir / 60) % 60))
                        seconds = str(int(fulldir % 60))
                        if len(seconds) == 1:
                            seconds = "0" + seconds
                        try:
                            message_data = str(self.botmessages['unpause_command_data'][0]).format(
                                str(self.player.title), str(self.player.uploader), minutes, seconds)
                            yield from client.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                        self.player.resume()
                    else:
                        try:
                            msgdata = str(self.botmessages['unpause_command_data'][1])
                            message_data = msgdata
                            yield from client.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    return
            else:
                message_data = str(self.botmessages['unpause_command_data'][2])
                yield from client.send_message(message.channel, content=message_data)
        if message.content.startswith(self._bot_prefix + 'move'):
            if message.author.id in self.banlist['Users']:
                return
            elif self.voice_message_channel is not None:
                if message.channel.id == self.voice_message_channel.id:
                    self.vchannel = message.author.voice_channel
                    bot = message.channel.server.get_member_named('{0}#{1}'.format(client.user.name,
                                                                                   client.user.discriminator))
                    try:
                        yield from client.move_member(bot, self.vchannel)
                        try:
                            message_data = str(self.botmessages['move_command_data'][0]).format(self.vchannel.name)
                            yield from client.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.errors.InvalidArgument:
                        try:
                            message_data = str(self.botmessages['move_command_data'][1])
                            yield from client.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.errors.Forbidden:
                        try:
                            msgdata = str(self.botmessages['move_command_data'][2]).format(self.vchannel.name)
                            message_data = msgdata
                            yield from client.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                        except discord.errors.HTTPException:
                            try:
                                message_data = str(self.botmessages['move_command_data'][3]).format(self.vchannel.name)
                                yield from client.send_message(self.voice_message_channel, content=message_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    return
        if message.content.startswith(self._bot_prefix + 'LeaveVoiceChannel'):
            if message.author.id in self.banlist['Users']:
                return
            elif self.voice is not None:
                if self.voice_message_channel is not None:
                    if message.channel.id == self.voice_message_channel.id:
                        try:
                            yield from self.voice.disconnect()
                        except ConnectionResetError:
                            # Supress a Error here.
                            pass
                        if self.vchannel is not None:
                            try:
                                self.botvoicechannel['Bot_Current_Voice_Channel'].remove(self.vchannel.id)
                            except ValueError:
                                pass
                            try:
                                self.botvoicechannel['Bot_Current_Voice_Channel'].remove(self.voice_message_server.id)
                            except ValueError:
                                pass
                            try:
                                self.botvoicechannel['Bot_Current_Voice_Channel'].remove(self.voice_message_channel.id)
                            except ValueError:
                                pass
                            try:
                                self.botvoicechannel['Bot_Current_Voice_Channel'].remove(self.voice_message_server_name)
                            except ValueError:
                                pass
                            try:
                                self.botvoicechannel['Bot_Current_Voice_Channel'].remove(self.vchannel_name)
                            except ValueError:
                                pass
                        filename = "{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json".format(self.path, self.sepa)
                        json.dump(self.botvoicechannel, open(filename, "w"))
                        try:
                            try:
                                message_data = str(self.botmessages['leave_voice_channel_command_data'][0]).format(
                                    self.vchannel.name)
                            except AttributeError:
                                message_data = str(self.botmessages['leave_voice_channel_command_data'][0]).format(
                                    self.vchannel_name)
                            yield from client.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                        self.vchannel = None
                        self.voice_message_channel = None
                        self.voice = None
                        self.vchannel_name = None
                        if self.player is not None:
                            self.player = None
                        self.voice_message_server = None
                        if self.is_bot_playing:
                            self.is_bot_playing = False
                    else:
                        return
            else:
                msgdata = str(self.botmessages['leave_voice_channel_command_data'][1])
                message_data = msgdata
                yield from client.send_message(message.channel, message_data)
        if message.content.startswith(self._bot_prefix + 'Playlist'):
            if message.author.id in self.banlist['Users']:
                return
            elif self.voice is not None:
                if self.voice_message_channel is not None:
                    if message.channel.id == self.voice_message_channel.id:
                        track1 = str(self.botmessages['playlist_command_data'][0])
                        track2 = str(self.botmessages['playlist_command_data'][0])
                        track3 = str(self.botmessages['playlist_command_data'][0])
                        track4 = str(self.botmessages['playlist_command_data'][0])
                        track5 = str(self.botmessages['playlist_command_data'][0])
                        track6 = str(self.botmessages['playlist_command_data'][0])
                        track7 = str(self.botmessages['playlist_command_data'][0])
                        track8 = str(self.botmessages['playlist_command_data'][0])
                        track9 = str(self.botmessages['playlist_command_data'][0])
                        track10 = str(self.botmessages['playlist_command_data'][0])
                        if len(self.bot_playlist_entries) == 0:
                            track1 = str(self.botmessages['playlist_command_data'][0])
                            track2 = str(self.botmessages['playlist_command_data'][0])
                            track3 = str(self.botmessages['playlist_command_data'][0])
                            track4 = str(self.botmessages['playlist_command_data'][0])
                            track5 = str(self.botmessages['playlist_command_data'][0])
                            track6 = str(self.botmessages['playlist_command_data'][0])
                            track7 = str(self.botmessages['playlist_command_data'][0])
                            track8 = str(self.botmessages['playlist_command_data'][0])
                            track9 = str(self.botmessages['playlist_command_data'][0])
                            track10 = str(self.botmessages['playlist_command_data'][0])
                        elif len(self.bot_playlist_entries) == 1:
                            track1 = str(self.bot_playlist_entries[0])
                            track2 = str(self.botmessages['playlist_command_data'][0])
                            track3 = str(self.botmessages['playlist_command_data'][0])
                            track4 = str(self.botmessages['playlist_command_data'][0])
                            track5 = str(self.botmessages['playlist_command_data'][0])
                            track6 = str(self.botmessages['playlist_command_data'][0])
                            track7 = str(self.botmessages['playlist_command_data'][0])
                            track8 = str(self.botmessages['playlist_command_data'][0])
                            track9 = str(self.botmessages['playlist_command_data'][0])
                            track10 = str(self.botmessages['playlist_command_data'][0])
                        elif len(self.bot_playlist_entries) == 2:
                            track1 = str(self.bot_playlist_entries[0])
                            track2 = str(self.bot_playlist_entries[1])
                            track3 = str(self.botmessages['playlist_command_data'][0])
                            track4 = str(self.botmessages['playlist_command_data'][0])
                            track5 = str(self.botmessages['playlist_command_data'][0])
                            track6 = str(self.botmessages['playlist_command_data'][0])
                            track7 = str(self.botmessages['playlist_command_data'][0])
                            track8 = str(self.botmessages['playlist_command_data'][0])
                            track9 = str(self.botmessages['playlist_command_data'][0])
                            track10 = str(self.botmessages['playlist_command_data'][0])
                        elif len(self.bot_playlist_entries) == 3:
                            track1 = str(self.bot_playlist_entries[0])
                            track2 = str(self.bot_playlist_entries[1])
                            track3 = str(self.bot_playlist_entries[2])
                            track4 = str(self.botmessages['playlist_command_data'][0])
                            track5 = str(self.botmessages['playlist_command_data'][0])
                            track6 = str(self.botmessages['playlist_command_data'][0])
                            track7 = str(self.botmessages['playlist_command_data'][0])
                            track8 = str(self.botmessages['playlist_command_data'][0])
                            track9 = str(self.botmessages['playlist_command_data'][0])
                            track10 = str(self.botmessages['playlist_command_data'][0])
                        elif len(self.bot_playlist_entries) == 4:
                            track1 = str(self.bot_playlist_entries[0])
                            track2 = str(self.bot_playlist_entries[1])
                            track3 = str(self.bot_playlist_entries[2])
                            track4 = str(self.bot_playlist_entries[3])
                            track5 = str(self.botmessages['playlist_command_data'][0])
                            track6 = str(self.botmessages['playlist_command_data'][0])
                            track7 = str(self.botmessages['playlist_command_data'][0])
                            track8 = str(self.botmessages['playlist_command_data'][0])
                            track9 = str(self.botmessages['playlist_command_data'][0])
                            track10 = str(self.botmessages['playlist_command_data'][0])
                        elif len(self.bot_playlist_entries) == 5:
                            track1 = str(self.bot_playlist_entries[0])
                            track2 = str(self.bot_playlist_entries[1])
                            track3 = str(self.bot_playlist_entries[2])
                            track4 = str(self.bot_playlist_entries[3])
                            track5 = str(self.bot_playlist_entries[4])
                            track6 = str(self.botmessages['playlist_command_data'][0])
                            track7 = str(self.botmessages['playlist_command_data'][0])
                            track8 = str(self.botmessages['playlist_command_data'][0])
                            track9 = str(self.botmessages['playlist_command_data'][0])
                            track10 = str(self.botmessages['playlist_command_data'][0])
                        elif len(self.bot_playlist_entries) == 6:
                            track1 = str(self.bot_playlist_entries[0])
                            track2 = str(self.bot_playlist_entries[1])
                            track3 = str(self.bot_playlist_entries[2])
                            track4 = str(self.bot_playlist_entries[3])
                            track5 = str(self.bot_playlist_entries[4])
                            track6 = str(self.bot_playlist_entries[5])
                            track7 = str(self.botmessages['playlist_command_data'][0])
                            track8 = str(self.botmessages['playlist_command_data'][0])
                            track9 = str(self.botmessages['playlist_command_data'][0])
                            track10 = str(self.botmessages['playlist_command_data'][0])
                        elif len(self.bot_playlist_entries) == 7:
                            track1 = str(self.bot_playlist_entries[0])
                            track2 = str(self.bot_playlist_entries[1])
                            track3 = str(self.bot_playlist_entries[2])
                            track4 = str(self.bot_playlist_entries[3])
                            track5 = str(self.bot_playlist_entries[4])
                            track6 = str(self.bot_playlist_entries[5])
                            track7 = str(self.bot_playlist_entries[6])
                            track8 = str(self.botmessages['playlist_command_data'][0])
                            track9 = str(self.botmessages['playlist_command_data'][0])
                            track10 = str(self.botmessages['playlist_command_data'][0])
                        elif len(self.bot_playlist_entries) == 8:
                            track1 = str(self.bot_playlist_entries[0])
                            track2 = str(self.bot_playlist_entries[1])
                            track3 = str(self.bot_playlist_entries[2])
                            track4 = str(self.bot_playlist_entries[3])
                            track5 = str(self.bot_playlist_entries[4])
                            track6 = str(self.bot_playlist_entries[5])
                            track7 = str(self.bot_playlist_entries[6])
                            track8 = str(self.bot_playlist_entries[7])
                            track9 = str(self.botmessages['playlist_command_data'][0])
                            track10 = str(self.botmessages['playlist_command_data'][0])
                        elif len(self.bot_playlist_entries) == 9:
                            track1 = str(self.bot_playlist_entries[0])
                            track2 = str(self.bot_playlist_entries[1])
                            track3 = str(self.bot_playlist_entries[2])
                            track4 = str(self.bot_playlist_entries[3])
                            track5 = str(self.bot_playlist_entries[4])
                            track6 = str(self.bot_playlist_entries[5])
                            track7 = str(self.bot_playlist_entries[6])
                            track8 = str(self.bot_playlist_entries[7])
                            track9 = str(self.bot_playlist_entries[8])
                            track10 = str(self.botmessages['playlist_command_data'][0])
                        elif len(self.bot_playlist_entries) == 10:
                            track1 = str(self.bot_playlist_entries[0])
                            track2 = str(self.bot_playlist_entries[1])
                            track3 = str(self.bot_playlist_entries[2])
                            track4 = str(self.bot_playlist_entries[3])
                            track5 = str(self.bot_playlist_entries[4])
                            track6 = str(self.bot_playlist_entries[5])
                            track7 = str(self.bot_playlist_entries[6])
                            track8 = str(self.bot_playlist_entries[7])
                            track9 = str(self.bot_playlist_entries[8])
                            track10 = str(self.bot_playlist_entries[9])
                        msgdata = str(self.botmessages['playlist_command_data'][1]).format(track1, track2, track3,
                                                                                           track4, track5, track6,
                                                                                           track7, track8, track9,
                                                                                           track10)
                        message_data = msgdata
                        yield from client.send_message(message.channel, content=message_data)
        if message.content.startswith(self._bot_prefix + "vol"):
            if message.author.id in self.banlist['Users']:
                return
            elif self.voice_message_channel is not None:
                if message.channel.id == self.voice_message_channel.id:
                    if self.player is not None:
                        value_string = message.content.strip(self._bot_prefix + "vol ")
                        try:
                            value = int(value_string) / 100
                            if 0.0 <= value <= 2.0:
                                self.player.volume = value
                                value_message = str(self.botmessages['volume_command_data'][0]).format(str(value * 100))
                                yield from client.send_message(self.voice_message_channel, content=value_message)
                            else:
                                yield from client.send_message(self.voice_message_channel,
                                                               content=str(self.botmessages['volume_command_data'][1]))
                        except ValueError:
                            yield from client.send_message(self.voice_message_channel,
                                                           content=str(self.botmessages['volume_command_data'][2]))
                else:
                    yield from client.send_message(self.voice_message_channel,
                                                   content=str(self.botmessages['volume_command_data'][3]))
        yield from self.playlist_iterator_code(client, message)

    @async
    def playlist_iterator_code(self, client, message):
        """
        Bot's Playlist code.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        if self.player is not None:
            if self.player.error is None:
                if self.voice_message_channel is not None:
                    if self.player.is_done():
                        fulldir = self.player.duration
                        minutes = str(int((fulldir / 60) % 60))
                        seconds = str(int(fulldir % 60))
                        if len(seconds) == 1:
                            seconds = "0" + seconds
                        if self._sent_finished_message is False:
                            self._sent_finished_message = True
                            self.is_bot_playing = False
                            # Clean the temp players now...
                            self.resolve_bot_playlist_issue()
                            try:
                                message_data = str(self.botmessages['auto_playlist_data'][0]).format(
                                    str(self.player.title), str(self.player.uploader), minutes, seconds)
                                yield from client.send_message(self.voice_message_channel, content=message_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                        if len(self.bot_playlist) == 0:
                            self.player = None
                        if len(self.bot_playlist) >= 1:
                            try:
                                track_data = None
                                try:
                                    track_data = str(self.bot_playlist_entries[0])
                                except IndexError:
                                    pass
                                data = str(self.bot_playlist[0])
                                try:
                                    self.player = yield from self.voice.create_ytdl_player(
                                        data, ytdl_options=self.ytdlo, options=self.ffmop)
                                except AttributeError:
                                    self.is_bot_playing = False
                                if self.player is not None:
                                    self._sent_finished_message = False
                                    try:
                                        self.bot_playlist.remove(data)
                                    except ValueError:
                                        pass
                                    try:
                                        self.bot_playlist_entries.remove(track_data)
                                    except ValueError:
                                        pass
                                    if self.is_bot_playing is False:
                                        self.is_bot_playing = True
                                        try:
                                            fulldir = self.player.duration
                                            minutes = str(int((fulldir / 60) % 60))
                                            seconds = str(int(fulldir % 60))
                                            if len(seconds) == 1:
                                                seconds = "0" + seconds
                                            track_info = str(self.botmessages['auto_playlist_data'][1]).format(
                                                str(self.player.title),
                                                str(self.player.uploader))
                                            message_data = str(self.botmessages['auto_playlist_data'][2]).format(
                                                track_info, minutes, seconds)
                                            yield from client.send_message(self.voice_message_channel,
                                                                           content=message_data)
                                            try:
                                                self.bot_playlist_entries.remove(track_info)
                                            except ValueError:
                                                pass
                                        except discord.errors.Forbidden:
                                            yield from BotPMError.resolve_send_message_error(client, message)
                                        if self.player is not None:
                                            self.player.start()
                            except UnboundLocalError:
                                self.is_bot_playing = False
            else:
                if self.voice_message_channel is not None:
                    # TODO: Fix this on being spammed when an exception happens. e.g. send once.
                    yield from client.send_message(self.voice_message_channel,
                                                   content="A Error Occured while playing. {0}".format(
                                                       self.player.error))

    @async
    def voice_stuff_new_disabled_code(self, client, message):
        """
            :rtype: Message object
            :param client: Discord.py Client Object
            :param message: Message Object
        """
        if message.content.startswith(self._bot_prefix + 'JoinVoiceChannel'):
            msgdata = str(self.botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, content=msgdata)
        if message.content.startswith(self._bot_prefix + 'play'):
            msgdata = str(self.botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, content=msgdata)
        if message.content.startswith(self._bot_prefix + 'stop'):
            msgdata = str(self.botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, content=msgdata)
        if message.content.startswith(self._bot_prefix + 'pause'):
            msgdata = str(self.botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, content=msgdata)
        if message.content.startswith(self._bot_prefix + 'unpause'):
            msgdata = str(self.botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, content=msgdata)
        if message.content.startswith(self._bot_prefix + 'move'):
            msgdata = str(self.botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, content=msgdata)
        if message.content.startswith(self._bot_prefix + 'LeaveVoiceChannel'):
            msgdata = str(self.botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, content=msgdata)
        if message.content.startswith(self._bot_prefix + 'Playlist'):
            msgdata = str(self.botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, content=msgdata)
        if message.content.startswith(self._bot_prefix + "vol"):
            msgdata = str(self.botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, content=msgdata)

    @async
    def reload_commands_bypass1_new_code(self, client, message, reload_reason):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Message.
        :param reload_reason: Reason for reloading.
        :return: Nothing.
        """
        if self.voice is not None:
            yield from self.voice.disconnect()
            if self.voice_message_channel is not None:
                try:
                    if reload_reason is not None:
                        try:
                            message_data = str(self.botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                self.vchannel.name, reload_reason)
                        except AttributeError:
                            message_data = str(self.botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                self.vchannel_name, reload_reason)
                    else:
                        reason = str(self.botmessages['reload_commands_voice_channels_bypass1'][1])
                        try:
                            message_data = str(self.botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                self.vchannel.name, reason)
                        except AttributeError:
                            message_data = str(self.botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                self.vchannel_name, reason)
                    yield from client.send_message(self.voice_message_channel, content=message_data)
                    self.voice_message_channel = None
                    self.voice = None
                    self.vchannel = None
                    self.voice_message_server = None
                    self.player = None
                    self.vchannel_name = None
                    self._sent_finished_message = False
                    self.voice_message_server_name = None
                    self.is_bot_playing = False
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)

    @async
    def reload_commands_bypass2_new_code(self, client, message):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        try:
            vchannel_2 = str(self.botvoicechannel['Bot_Current_Voice_Channel'][0])
            vmserver = str(self.botvoicechannel['Bot_Current_Voice_Channel'][1])
            vmchannel = str(self.botvoicechannel['Bot_Current_Voice_Channel'][2])
            self.voice_message_server_name = str(self.botvoicechannel['Bot_Current_Voice_Channel'][3])
            self.vchannel_name = str(self.botvoicechannel['Bot_Current_Voice_Channel'][4])
            self.vchannel = discord.Object(id=vchannel_2)
            self.voice_message_server = discord.Object(id=vmserver)
            self.voice_message_channel = discord.Object(id=vmchannel)
            try:
                self.voice = yield from client.join_voice_channel(self.vchannel)
                self.verror = False
            except discord.errors.ConnectionClosed:
                pass
            except discord.errors.InvalidArgument:
                self.voice_message_server_name = None
                self.vchannel_name = None
                self.vchannel = None
                self.voice_message_server = None
                self.voice_message_channel = None
                self.voice = None
                self.verror = True
            except BotErrors.CommandTimeoutError:
                yield from client.send_message(message.channel,
                                               content=str(
                                                   self.botmessages['reload_commands_voice_channels_bypass2'][0]))
                self.voice_message_server_name = None
                self.vchannel_name = None
                self.vchannel = None
                self.voice_message_server = None
                self.voice_message_channel = None
                self.voice = None
                self.verror = True
            except RuntimeError:
                self.voice_message_server_name = None
                self.vchannel_name = None
                self.vchannel = None
                self.voice_message_server = None
                self.voice_message_channel = None
                self.voice = None
                self.verror = True
                msgdata = str(self.botmessages['reload_commands_voice_channels_bypass2'][1])
                yield from client.send_message(self.voice_message_channel, content=msgdata)
            if self.verror is not True:
                message_data = str(self.botmessages['reload_commands_voice_channels_bypass2'][2]).format(
                    self.vchannel_name)
                yield from client.send_message(self.voice_message_channel, content=message_data)
        except IndexError:
            self.voice_message_server_name = None
            self.vchannel_name = None
            self.vchannel = None
            self.voice_message_server = None
            self.voice_message_channel = None
            self.voice = None

    @async
    def reload_commands_bypass3_new_code(self, client):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :return: Nothing.
        """
        self.lock_join_voice_channel_command = True
        try:
            vchannel_2 = str(self.botvoicechannel['Bot_Current_Voice_Channel'][0])
            vmserver = str(self.botvoicechannel['Bot_Current_Voice_Channel'][1])
            vmchannel = str(self.botvoicechannel['Bot_Current_Voice_Channel'][2])
            self.voice_message_server_name = str(self.botvoicechannel['Bot_Current_Voice_Channel'][3])
            self.vchannel_name = str(self.botvoicechannel['Bot_Current_Voice_Channel'][4])
            self.vchannel = discord.Object(id=vchannel_2)
            self.voice_message_server = discord.Object(id=vmserver)
            self.voice_message_channel = discord.Object(id=vmchannel)
            discord.opus.load_opus(self.opusdll)
            try:
                self.voice = yield from client.join_voice_channel(self.vchannel)
                self.verror = False
            except discord.errors.ConnectionClosed:
                pass
#            except discord.errors.InvalidServerError:
#                self.voice_message_server_name = None
#                self.vchannel_name = None
#                self.vchannel = None
#                self.voice_message_server = None
#                self.voice_message_channel = None
#                self.voice = None
#                self.verror = True
#                self.lock_join_voice_channel_command = False
            except discord.errors.InvalidArgument:
                self.voice_message_server_name = None
                self.vchannel_name = None
                self.vchannel = None
                self.voice_message_server = None
                self.voice_message_channel = None
                self.voice = None
                self.verror = True
                self.lock_join_voice_channel_command = False
            except RuntimeError:
                self.voice_message_server_name = None
                self.vchannel_name = None
                self.vchannel = None
                self.voice_message_server = None
                self.voice_message_channel = None
                self.voice = None
                self.verror = True
                self.lock_join_voice_channel_command = False
                msgdata = str(self.botmessages['reload_commands_voice_channels_bypass2'][1])
                yield from client.send_message(self.voice_message_channel, content=msgdata)
            if self.verror is not True:
                message_data = str(self.botmessages['reload_commands_voice_channels_bypass2'][2]).format(
                    self.vchannel_name)
                yield from client.send_message(self.voice_message_channel, content=message_data)
                self.lock_join_voice_channel_command = False
        except IndexError:
            self.voice_message_server_name = None
            self.vchannel_name = None
            self.vchannel = None
            self.voice_message_server = None
            self.voice_message_channel = None
            self.voice = None
            self.lock_join_voice_channel_command = False

    @async
    def reload_commands_bypass4_new_code(self, client, message, reload_reason):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Message.
        :param reload_reason: Reason for reloading.
        :return: Nothing.
        """
        if self.voice is not None:
            yield from self.voice.disconnect()
            if self.voice_message_channel is not None:
                try:
                    if reload_reason is not None:
                        try:
                            message_data = str(self.botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                self.vchannel.name, reload_reason)
                        except AttributeError:
                            message_data = str(self.botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                self.vchannel_name, reload_reason)
                    else:
                        reason = str(self.botmessages['reload_commands_voice_channels_bypass4'][0])
                        try:
                            message_data = str(self.botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                self.vchannel.name, reason)
                        except AttributeError:
                            message_data = str(self.botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                self.vchannel_name, reason)
                    yield from client.send_message(self.voice_message_channel, content=message_data)
                    self.voice_message_channel = None
                    self.voice = None
                    self.vchannel = None
                    self.voice_message_server = None
                    self.player = None
                    self.vchannel_name = None
                    self._sent_finished_message = False
                    self.voice_message_server_name = None
                    self.is_bot_playing = False
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)


class VoiceBotCommands(BotData):
    """
    Class for Voice Channel Functionality in this bot.
    """
    def __init__(self):
        super(VoiceBotCommands, self).__init__()

    @async
    def voice_stuff_new(self, client, message):
        """
        Listens for the Voice Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.voice_stuff_new_code(client, message)

    @async
    def voice_stuff_new_disabled(self, client, message):
        """
        This is a Dummy function for disabling Voice channel stuffs when Discord.py has disconnect bugs.

        I am sorry for Any Inconvience however these bugs are because of Rapptz's Discord.py.

        To shut PyCharm the fuck up below.
        :param client:
        :param message:
        """
        yield from self.voice_stuff_new_disabled_code(client, message)

    @async
    def reload_commands_bypass1_new(self, client, message, reload_reason):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Message.
        :param reload_reason: Reason for reloading.
        :return: Nothing.
        """
        yield from self.reload_commands_bypass1_new_code(client, message, reload_reason)

    @async
    def reload_commands_bypass2_new(self, client, message):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.reload_commands_bypass2_new_code(client, message)

    @async
    def reload_commands_bypass3_new(self, client):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :return: Nothing.
        """
        yield from self.reload_commands_bypass3_new_code(client)

    @async
    def reload_commands_bypass4_new(self, client, message, reload_reason):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Message.
        :param reload_reason: Reason for reloading.
        :return: Nothing.
        """
        yield from self.reload_commands_bypass4_new_code(client, message, reload_reason)
