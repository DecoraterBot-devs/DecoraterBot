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
import asyncio
import json
import io
import sys
import os
import os.path
import concurrent
import youtube_dl
import ctypes
import BotPMError
from discord.ext import commands

sepa = os.sep

botbanslist = io.open('{0}{1}resources{1}ConfigData{1}BotBanned.json'.format(sys.path[0], sepa))
banlist = json.load(botbanslist)
botbanslist.close()
try:
    botvoicechannelfile = io.open('{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json'.format(sys.path[0], sepa))
    botvoicechannel = json.load(botvoicechannelfile)
    botvoicechannelfile.close()
except FileNotFoundError:
    pass
botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.json'.format(sys.path[0], sepa))
botmessages = json.load(botmessagesdata)
botmessagesdata.close()

PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(sys.path[0], sepa)
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    credsfile = io.open(PATH)
    credentials = json.load(credsfile)
    credsfile.close()
    _bot_prefix = str(credentials['bot_prefix'][0])
    _log_ytdl = str(credentials['ytdl_logs'][0])
    if _log_ytdl == 'True':
        _log_ytdl = True
    elif _log_ytdl == 'False':
        _log_ytdl = False

bits = ctypes.sizeof(ctypes.c_voidp)
if bits == 4:
    if not (sys.platform.startswith('linux')):
        opusdll = '{0}{1}resources{1}opus{1}win32{1}x86{1}opus.dll'.format(sys.path[0], sepa)
        os.chdir('{0}{1}resources{1}ffmpeg{1}win32{1}x86'.format(sys.path[0], sepa))
    else:
        opusdll = '{0}{1}resources{1}opus{1}linux{1}x86{1}opus.dll'.format(sys.path[0], sepa)
        os.chdir('{0}{1}resources{1}ffmpeg{1}linux{1}x86'.format(sys.path[0], sepa))
elif bits == 8:
    if not (sys.platform.startswith('linux')):
        opusdll = '{0}{1}resources{1}opus{1}win32{1}x64{1}opus.dll'.format(sys.path[0], sepa)
        os.chdir('{0}{1}resources{1}ffmpeg{1}win32(1)x64'.format(sys.path[0], sepa))
    else:
        opusdll = '{0}{1}resources{1}opus{1}linux{1}x64{1}opus.dll'.format(sys.path[0], sepa)
        os.chdir('{0}{1}resources{1}ffmpeg{1}linux{1}x64'.format(sys.path[0], sepa))


class YTDLLogger(object):
    """
    Class for Silencing all of the Youtube_DL Logging stuff that defaults to console.
    """
    @staticmethod
    def log_file_code(meth, msg):
        """
        Logs data to file (if set).
        :param meth: Method name.
        :param msg: message.
        :return: Nothing.
        """
        if meth is not '':
            if meth == 'ytdl_debug':
                logfile = '{0}{1}resources{1}Logs{1}ytdl_debug_logs.txt'.format(sys.path[0], sepa)
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
                logfile2 = '{0}{1}resources{1}Logs{1}ytdl_warning_logs.txt'.format(sys.path[0], sepa)
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
                logfile3 = '{0}{1}resources{1}Logs{1}ytdl_error_logs.txt'.format(sys.path[0], sepa)
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
                logfile4 = '{0}{1}resources{1}Logs{1}ytdl_info_logs.txt'.format(sys.path[0], sepa)
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
        if _log_ytdl:
            self.log_file_code('ytdl_info', msg)
        else:
            pass

    def debug(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if _log_ytdl:
            self.log_file_code('ytdl_debug', msg)
        else:
            pass

    def warning(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if _log_ytdl:
            self.log_file_code('ytdl_warning', msg)
        else:
            pass

    def error(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if _log_ytdl:
            self.log_file_code('ytdl_error', msg)
        else:
            pass


global ytdlo
global player
global vchannel
global vchannel_name
global voice_message_channel
global voice_message_server
global voice_message_server_name
global voice
global _sent_finished_message
global sent_prune_error_message
global is_bot_playing
global bot_playlist
global bot_playlist_entries
global _temp_player_1
global _temp_player_2
global _temp_player_3
global _temp_player_4
global _temp_player_5
global _temp_player_6
global _temp_player_7
global _temp_player_8
global _temp_player_9
global _temp_player_10
global ffmop
global ffmout
global verror

ytdlo = {'verbose': False, 'logger': YTDLLogger(), 'default_search': "ytsearch"}
player = None
vchannel = None
vchannel_name = None
voice_message_channel = None
voice_message_server = None
voice_message_server_name = None
voice = None
_sent_finished_message = False
sent_prune_error_message = False
is_bot_playing = False
bot_playlist = []
bot_playlist_entries = []
_temp_player_1 = None
_temp_player_2 = None
_temp_player_3 = None
_temp_player_4 = None
_temp_player_5 = None
_temp_player_6 = None
_temp_player_7 = None
_temp_player_8 = None
_temp_player_9 = None
_temp_player_10 = None
ffmop = "-nostats -loglevel quiet"
ffmout = io.open('{0}{1}resources{1}Logs{1}ffmpeg.shit'.format(sys.path[0], sepa), 'w')
verror = False


class BotData:
    """
        This class is for Internal use only!!!
    """
    def __init__(self):
        pass

    @asyncio.coroutine
    def voice_stuff_new_code(self, client, message):
        """
        Listens for the Voice Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        global player
        global vchannel
        global vchannel_name
        global voice_message_channel
        global voice
        global _sent_finished_message
        global voice_message_server
        global is_bot_playing
        global bot_playlist
        global _temp_player_1
        global _temp_player_2
        global _temp_player_3
        global _temp_player_4
        global _temp_player_5
        global _temp_player_6
        global _temp_player_7
        global _temp_player_8
        global _temp_player_9
        global _temp_player_10
        global bot_playlist_entries
        global ffmop
        global ffmout
        global voice_message_server_name
        global verror
        if message.content.startswith(_bot_prefix + 'JoinVoiceChannel'):
            if message.author.id in banlist['Users']:
                return
            elif vchannel is not None:
                try:
                    messagedata = str(botmessages['join_voice_channel_command_data'][0])
                    try:
                        message_data = messagedata.format(voice_message_server.name)
                    except AttributeError:
                        message_data = messagedata.format(voice_message_server_name)
                    yield from client.send_message(message.channel, message_data)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)
            else:
                discord.opus.load_opus(opusdll)
                voice_message_channel = message.channel
                voice_message_server = message.channel.server
                voice_message_server_name = message.channel.server.name
                if message.author.voice_channel is not None:
                    vchannel = message.author.voice_channel
                    vchannel_name = message.author.voice_channel.name
                    if vchannel.id not in botvoicechannel:
                        botvoicechannel['Bot_Current_Voice_Channel'].append(vchannel.id)
                    if voice_message_server.id not in botvoicechannel:
                        botvoicechannel['Bot_Current_Voice_Channel'].append(voice_message_server.id)
                    if voice_message_channel.id not in botvoicechannel:
                        botvoicechannel['Bot_Current_Voice_Channel'].append(voice_message_channel.id)
                    if voice_message_server_name not in botvoicechannel:
                        botvoicechannel['Bot_Current_Voice_Channel'].append(voice_message_server_name)
                    if vchannel_name not in botvoicechannel:
                        botvoicechannel['Bot_Current_Voice_Channel'].append(vchannel_name)
                    file_name = "{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json".format(sys.path[0], sepa)
                    json.dump(botvoicechannel, open(file_name, "w"))
                    try:
                        try:
                            voice = yield from client.join_voice_channel(vchannel)
                        except discord.errors.ConnectionClosed:
                            pass
                        except RuntimeError:
                            voice_message_server_name = None
                            vchannel_name = None
                            vchannel = None
                            voice_message_server = None
                            voice_message_channel = None
                            voice = None
                            verror = True
                            msgdata = str(botmessages['join_voice_channel_command_data'][6])
                            yield from client.send_message(voice_message_channel, msgdata)
                        if not verror:
                            try:
                                msg_data = str(botmessages['join_voice_channel_command_data'][1]).format(vchannel.name)
                                yield from client.send_message(message.channel, msg_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.errors.InvalidArgument:
                        voice_message_channel = None
                        voice = None
                        vchannel = None
                        voice_message_server = None
                        voice_message_server_name = None
                        vchannel_name = None
                        try:
                            msg_data = str(botmessages['join_voice_channel_command_data'][2])
                            yield from client.send_message(message.channel, msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except asyncio.TimeoutError:
                        voice_message_channel = None
                        voice = None
                        vchannel = None
                        voice_message_server = None
                        voice_message_server_name = None
                        vchannel_name = None
                        try:
                            msg_data = str(botmessages['join_voice_channel_command_data'][3])
                            yield from client.send_message(message.channel, msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.errors.ClientException:
                        voice_message_channel = None
                        voice = None
                        vchannel = None
                        voice_message_server = None
                        try:
                            msg_data = str(botmessages['join_voice_channel_command_data'][4])
                            yield from client.send_message(message.channel, msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.opus.OpusNotLoaded:
                        voice_message_channel = None
                        voice = None
                        vchannel = None
                        voice_message_server = None
                        voice_message_server_name = None
                        vchannel_name = None
                        try:
                            msg_data = str(botmessages['join_voice_channel_command_data'][5])
                            yield from client.send_message(message.channel, msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except IndexError:
                        return
        if message.content.startswith(_bot_prefix + 'play'):
            if message.author.id in banlist['Users']:
                return
            elif is_bot_playing is False:
                if voice is not None:
                    if voice_message_channel is not None:
                        if message.channel.id == voice_message_channel.id:
                            try:
                                data = message.content[len(_bot_prefix + "play "):].strip()
                                if data == "":
                                    try:
                                        message_data = str(botmessages['play_command_data'][0])
                                        yield from client.send_message(voice_message_channel, message_data)
                                    except discord.errors.Forbidden:
                                        yield from BotPMError.resolve_send_message_error(client, message)
                                if data.rfind('https://') == -1 and data.rfind('http://') == -1:
                                    # lets try to do a search.
                                    player = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                 options=ffmop, output=ffmout)
                                    _sent_finished_message = False
                                    is_bot_playing = True
                                    if player is not None:
                                        try:
                                            fulldir = player.duration
                                            minutes = str(int((fulldir / 60) % 60))
                                            seconds = str(int(fulldir % 60))
                                            if len(seconds) == 1:
                                                seconds = "0" + seconds
                                            try:
                                                message_data = str(botmessages['play_command_data'][1]).format(
                                                    str(player.title), str(player.uploader), minutes, seconds)
                                                yield from client.send_message(voice_message_channel, message_data)
                                            except discord.errors.Forbidden:
                                                yield from BotPMError.resolve_send_message_error(client, message)
                                            try:
                                                player.start()
                                            except RuntimeError:
                                                pass
                                        except AttributeError:
                                            message_data = str(botmessages['play_command_data'][2])
                                            is_bot_playing = False
                                            yield from client.send_message(voice_message_channel, message_data)
                                else:
                                    if '<' and '>' in data:
                                        data = data.strip('<')
                                        data = data.strip('>')
                                    if 'www.youtube.com/watch?v=' in data:
                                        player = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                        _sent_finished_message = False
                                        is_bot_playing = True
                                        if player is not None:
                                            try:
                                                fulldir = player.duration
                                                minutes = str(int((fulldir / 60) % 60))
                                                seconds = str(int(fulldir % 60))
                                                if len(seconds) == 1:
                                                    seconds = "0" + seconds
                                                try:
                                                    message_data = str(botmessages['play_command_data'][1]).format(
                                                        str(player.title), str(player.uploader), minutes, seconds)
                                                    yield from client.send_message(voice_message_channel,
                                                                                   message_data)
                                                except discord.errors.Forbidden:
                                                    yield from BotPMError.resolve_send_message_error(client, message)
                                                try:
                                                    player.start()
                                                except RuntimeError:
                                                    pass
                                            except AttributeError:
                                                message_data = str(botmessages['play_command_data'][2])
                                                is_bot_playing = False
                                                yield from client.send_message(voice_message_channel, message_data)
                                    else:
                                        message_data = str(botmessages['play_command_data'][3])
                                        yield from client.send_message(voice_message_channel, message_data)
                                        _temp_player_1 = None
                            except IndexError:
                                return
                            except discord.errors.ClientException:
                                message_data = str(botmessages['play_command_data'][4]).format(str(sys.path))
                                yield from client.send_message(message.channel, message_data)
                                player = None
                            except youtube_dl.utils.UnsupportedError:
                                yield from client.send_message(message.channel,
                                                               str(botmessages['play_command_data'][5]))
                                player = None
                            except youtube_dl.utils.ExtractorError:
                                message_data = str(botmessages['play_command_data'][6])
                                yield from client.send_message(message.channel, message_data)
                                player = None
                            except youtube_dl.utils.DownloadError:
                                yield from client.send_message(message.channel,
                                                               str(botmessages['play_command_data'][7]))
                                player = None
                        else:
                            return
                else:
                    message_data = str(botmessages['play_command_data'][8])
                    yield from client.send_message(message.channel, message_data)
            else:
                if player is not None:
                    data = message.content[len(_bot_prefix + "play "):].strip()
                    if data == "":
                        try:
                            message_data = str(botmessages['play_command_data'][9])
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    else:
                        if '<' and '>' in data:
                            data = data.replace('<', '').replace('>', '')
                        if 'www.youtube.com/watch?v=' in data:
                            if len(bot_playlist) == 0:
                                _temp_player_1 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist01 = _temp_player_1.title
                                    playlist01time = _temp_player_1.duration
                                    track1 = str(botmessages['play_command_data'][10]).format(playlist01)
                                    fulldir = playlist01time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track1time = newdir
                                    track1uploader = str(_temp_player_1.uploader)
                                    track1info = str(botmessages['play_command_data'][12]).format(track1,
                                                                                                  track1uploader,
                                                                                                  track1time)
                                    bot_playlist_entries.append(track1info)
                                    msgdata = str(botmessages['play_command_data'][13]).format(track1, track1time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    # Thread Exception here when it gets to this line when the normal "player" is
                                    # playing. I need some workarround to clear the temp players.
                                    _temp_player_1.start()
                                    _temp_player_1.stop()
                                except AttributeError:
                                    message_data = str(botmessages['play_command_data'][2])
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif data in bot_playlist:
                                msgdata = str(botmessages['play_command_data'][14])
                                message_data = msgdata
                                yield from client.send_message(message.channel, message_data)
                            elif len(bot_playlist) == 1:
                                _temp_player_2 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist02 = _temp_player_2.title
                                    playlist02time = _temp_player_2.duration
                                    track2 = str(botmessages['play_command_data'][10]).format(playlist02)
                                    fulldir = playlist02time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track2time = newdir
                                    track2uploader = str(_temp_player_2.uploader)
                                    track2info = str(botmessages['play_command_data'][12]).format(track2,
                                                                                                  track2uploader,
                                                                                                  track2time)
                                    bot_playlist_entries.append(track2info)
                                    msgdata = str(botmessages['play_command_data'][13]).format(track2, track2time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    # Thread Exception here when it gets to this line when the normal "player" is
                                    # playing. I need some workarround to clear the temp players.
                                    _temp_player_2.start()
                                    _temp_player_2.stop()
                                except AttributeError:
                                    message_data = str(botmessages['play_command_data'][2])
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 2:
                                _temp_player_3 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist03 = _temp_player_3.title
                                    playlist03time = _temp_player_3.duration
                                    track3 = str(botmessages['play_command_data'][10]).format(playlist03)
                                    fulldir = playlist03time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track3time = newdir
                                    track3uploader = str(_temp_player_3.uploader)
                                    track3info = str(botmessages['play_command_data'][12]).format(track3,
                                                                                                  track3uploader,
                                                                                                  track3time)
                                    bot_playlist_entries.append(track3info)
                                    msgdata = str(botmessages['play_command_data'][13]).format(track3, track3time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    # Thread Exception here when it gets to this line when the normal "player" is
                                    # playing. I need some workarround to clear the temp players.
                                    _temp_player_3.start()
                                    _temp_player_3.stop()
                                except AttributeError:
                                    message_data = str(botmessages['play_command_data'][2])
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 3:
                                _temp_player_4 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist04 = _temp_player_4.title
                                    playlist04time = _temp_player_4.duration
                                    track4 = str(botmessages['play_command_data'][10]).format(playlist04)
                                    fulldir = playlist04time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track4time = newdir
                                    track4uploader = str(_temp_player_4.uploader)
                                    track4info = str(botmessages['play_command_data'][12]).format(track4,
                                                                                                  track4uploader,
                                                                                                  track4time)
                                    bot_playlist_entries.append(track4info)
                                    msgdata = str(botmessages['play_command_data'][13]).format(track4, track4time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    # Thread Exception here when it gets to this line when the normal "player" is
                                    # playing. I need some workarround to clear the temp players.
                                    _temp_player_4.start()
                                    _temp_player_4.stop()
                                except AttributeError:
                                    message_data = str(botmessages['play_command_data'][2])
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 4:
                                _temp_player_5 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist05 = _temp_player_5.title
                                    playlist05time = _temp_player_5.duration
                                    track5 = str(botmessages['play_command_data'][10]).format(playlist05)
                                    fulldir = playlist05time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track5time = newdir
                                    track5uploader = str(_temp_player_5.uploader)
                                    track5info = str(botmessages['play_command_data'][12]).format(track5,
                                                                                                  track5uploader,
                                                                                                  track5time)
                                    bot_playlist_entries.append(track5info)
                                    msgdata = str(botmessages['play_command_data'][13]).format(track5, track5time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    # Thread Exception here when it gets to this line when the normal "player" is
                                    # playing. I need some workarround to clear the temp players.
                                    _temp_player_5.start()
                                    _temp_player_5.stop()
                                except AttributeError:
                                    message_data = str(botmessages['play_command_data'][2])
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 5:
                                _temp_player_6 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist06 = _temp_player_6.title
                                    playlist06time = _temp_player_6.duration
                                    track6 = str(botmessages['play_command_data'][10]).format(playlist06)
                                    fulldir = playlist06time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track6time = newdir
                                    track6uploader = str(_temp_player_6.uploader)
                                    track6info = str(botmessages['play_command_data'][12]).format(track6,
                                                                                                  track6uploader,
                                                                                                  track6time)
                                    bot_playlist_entries.append(track6info)
                                    msgdata = str(botmessages['play_command_data'][13]).format(track6, track6time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    # Thread Exception here when it gets to this line when the normal "player" is
                                    # playing. I need some workarround to clear the temp players.
                                    _temp_player_6.start()
                                    _temp_player_6.stop()
                                except AttributeError:
                                    message_data = str(botmessages['play_command_data'][2])
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 6:
                                _temp_player_7 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist07 = _temp_player_7.title
                                    playlist07time = _temp_player_7.duration
                                    track7 = str(botmessages['play_command_data'][10]).format(playlist07)
                                    fulldir = playlist07time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track7time = newdir
                                    track7uploader = str(_temp_player_7.uploader)
                                    track7info = str(botmessages['play_command_data'][12]).format(track7,
                                                                                                  track7uploader,
                                                                                                  track7time)
                                    bot_playlist_entries.append(track7info)
                                    msgdata = str(botmessages['play_command_data'][13]).format(track7, track7time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    # Thread Exception here when it gets to this line when the normal "player" is
                                    # playing. I need some workarround to clear the temp players.
                                    _temp_player_7.start()
                                    _temp_player_7.stop()
                                except AttributeError:
                                    message_data = str(botmessages['play_command_data'][2])
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 7:
                                _temp_player_8 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist08 = _temp_player_8.title
                                    playlist08time = _temp_player_8.duration
                                    track8 = str(botmessages['play_command_data'][10]).format(playlist08)
                                    fulldir = playlist08time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track8time = newdir
                                    track8uploader = str(_temp_player_8.uploader)
                                    track8info = str(botmessages['play_command_data'][12]).format(track8,
                                                                                                  track8uploader,
                                                                                                  track8time)
                                    bot_playlist_entries.append(track8info)
                                    msgdata = str(botmessages['play_command_data'][13]).format(track8, track8time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    # Thread Exception here when it gets to this line when the normal "player" is
                                    # playing. I need some workarround to clear the temp players.
                                    _temp_player_8.start()
                                    _temp_player_8.stop()
                                except AttributeError:
                                    message_data = str(botmessages['play_command_data'][2])
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 8:
                                _temp_player_9 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist09 = _temp_player_9.title
                                    playlist09time = _temp_player_9.duration
                                    track9 = str(botmessages['play_command_data'][10]).format(playlist09)
                                    fulldir = playlist09time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track9time = newdir
                                    track9uploader = str(_temp_player_9.uploader)
                                    track9info = str(botmessages['play_command_data'][12]).format(track9,
                                                                                                  track9uploader,
                                                                                                  track9time)
                                    bot_playlist_entries.append(track9info)
                                    msgdata = str(botmessages['play_command_data'][13]).format(track9, track9time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    # Thread Exception here when it gets to this line when the normal "player" is
                                    # playing. I need some workarround to clear the temp players.
                                    _temp_player_9.start()
                                    _temp_player_9.stop()
                                except AttributeError:
                                    message_data = str(botmessages['play_command_data'][2])
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 9:
                                _temp_player_10 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                      options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist10 = _temp_player_10.title
                                    playlist10time = _temp_player_10.duration
                                    track10 = str(botmessages['play_command_data'][10]).format(playlist10)
                                    fulldir = playlist10time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = str(botmessages['play_command_data'][11]).format(minutes, seconds)
                                    track10time = newdir
                                    track10uploader = str(_temp_player_10.uploader)
                                    track10info = str(botmessages['play_command_data'][12]).format(track10,
                                                                                                   rack10uploader,
                                                                                                   track10time)
                                    bot_playlist_entries.append(track10info)
                                    msgdata = str(botmessages['play_command_data'][13]).format(track10, track10time)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    # Thread Exception here when it gets to this line when the normal "player" is
                                    # playing. I need some workarround to clear the temp players.
                                    _temp_player_10.start()
                                    _temp_player_10.stop()
                                except AttributeError:
                                    message_data = str(botmessages['play_command_data'][2])
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 10:
                                msgdata = str(botmessages['play_command_data'][15])
                                message_data = msgdata
                                yield from client.send_message(message.channel, message_data)
        if message.content.startswith(_bot_prefix + 'stop'):
            if message.author.id in banlist['Users']:
                return
            elif voice_message_channel is not None:
                if message.channel.id == voice_message_channel.id:
                    if player is not None:
                        fulldir = player.duration
                        minutes = str(int((fulldir / 60) % 60))
                        seconds = str(int(fulldir % 60))
                        if len(seconds) == 1:
                            seconds = "0" + seconds
                        try:
                            message_data = str(botmessages['stop_command_data'][0]).format(str(player.title),
                                                                                           str(player.uploader),
                                                                                           minutes, seconds)
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                        player.stop()
                        player = None
                        is_bot_playing = False
                        if len(bot_playlist) >= 1:
                            try:
                                track_data = None
                                try:
                                    track_data = str(bot_playlist_entries[0])
                                except IndexError:
                                    pass
                                data = str(bot_playlist[0])
                                player = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                             options=ffmop, output=ffmout)
                                if player is not None:
                                    _sent_finished_message = False
                                    try:
                                        bot_playlist.remove(data)
                                        bot_playlist_entries.remove(track_data)
                                    except ValueError:
                                        pass
                                    if is_bot_playing is False:
                                        is_bot_playing = True
                                        try:
                                            fulldir = player.duration
                                            minutes = str(int((fulldir / 60) % 60))
                                            seconds = str(int(fulldir % 60))
                                            if len(seconds) == 1:
                                                seconds = "0" + seconds
                                            track_info = str(botmessages['stop_command_data'][1]).format(
                                                str(player.title),
                                                str(player.uploader))
                                            message_data = str(botmessages['stop_command_data'][2]).format(track_info,
                                                                                                           minutes,
                                                                                                           seconds)
                                            yield from client.send_message(voice_message_channel, message_data)
                                            try:
                                                bot_playlist_entries.remove(track_info)
                                            except ValueError:
                                                pass
                                        except discord.errors.Forbidden:
                                            yield from BotPMError.resolve_send_message_error(client, message)
                                        player.start()
                            except UnboundLocalError:
                                player = None
                                is_bot_playing = False
                    else:
                        try:
                            message_data = str(botmessages['stop_command_data'][3])
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    return
        if message.content.startswith(_bot_prefix + 'pause'):
            if message.author.id in banlist['Users']:
                return
            elif voice_message_channel is not None:
                if message.channel.id == voice_message_channel.id:
                    if player is not None:
                        fulldir = player.duration
                        minutes = str(int((fulldir / 60) % 60))
                        seconds = str(int(fulldir % 60))
                        if len(seconds) == 1:
                            seconds = "0" + seconds
                        try:
                            message_data = str(botmessages['pause_command_data'][0]).format(
                                str(player.title), str(player.uploader), minutes, seconds)
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                        player.pause()
                    else:
                        message_data = str(botmessages['pause_command_data'][1])
                        yield from client.send_message(voice_message_channel, message_data)
                else:
                    return
            else:
                message_data = str(botmessages['pause_command_data'][2])
                yield from client.send_message(message.channel, message_data)
        if message.content.startswith(_bot_prefix + 'unpause'):
            if message.author.id in banlist['Users']:
                return
            elif voice_message_channel is not None:
                if message.channel.id == voice_message_channel.id:
                    if player is not None:
                        fulldir = player.duration
                        minutes = str(int((fulldir / 60) % 60))
                        seconds = str(int(fulldir % 60))
                        if len(seconds) == 1:
                            seconds = "0" + seconds
                        try:
                            message_data = str(botmessages['unpause_command_data'][0]).format(
                                str(player.title), str(player.uploader), minutes, seconds)
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                        player.resume()
                    else:
                        try:
                            msgdata = str(botmessages['unpause_command_data'][1])
                            message_data = msgdata
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    return
            else:
                message_data = str(botmessages['unpause_command_data'][2])
                yield from client.send_message(message.channel, message_data)
        if message.content.startswith(_bot_prefix + 'move'):
            if message.author.id in banlist['Users']:
                return
            elif voice_message_channel is not None:
                if message.channel.id == voice_message_channel.id:
                    vchannel = message.author.voice_channel
                    bot = message.channel.server.get_member_named('DecoraterBot#5102')
                    try:
                        yield from client.move_member(bot, vchannel)
                        try:
                            message_data = str(botmessages['move_command_data'][0]).format(vchannel.name)
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.errors.InvalidArgument:
                        try:
                            message_data = str(botmessages['move_command_data'][1])
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.errors.Forbidden:
                        try:
                            msgdata = str(botmessages['move_command_data'][2]).format(vchannel.name)
                            message_data = msgdata
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                        except discord.errors.HTTPException:
                            try:
                                message_data = 'Failed to move to the ' + vchannel.name + ' Voice Channel.'
                                yield from client.send_message(voice_message_channel, message_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    return
        if player is not None:
            if voice_message_channel is not None:
                if player.is_done() is not False:
                    fulldir = player.duration
                    minutes = str(int((fulldir / 60) % 60))
                    seconds = str(int(fulldir % 60))
                    if len(seconds) == 1:
                        seconds = "0" + seconds
                    if _sent_finished_message is False:
                        _sent_finished_message = True
                        is_bot_playing = False
                        try:
                            message_data = str(botmessages['auto_playlist_data'][0]).format(
                                str(player.title), str(player.uploader), minutes, seconds)
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    if len(bot_playlist) == 0:
                        player = None
                    if len(bot_playlist) >= 1:
                        try:
                            track_data = None
                            try:
                                track_data = str(bot_playlist_entries[0])
                            except IndexError:
                                pass
                            data = str(bot_playlist[0])
                            try:
                                player = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                             options=ffmop, output=ffmout)
                            except AttributeError:
                                is_bot_playing = False
                            if player is not None:
                                _sent_finished_message = False
                                try:
                                    bot_playlist.remove(data)
                                except ValueError:
                                    pass
                                try:
                                    bot_playlist_entries.remove(track_data)
                                except ValueError:
                                    pass
                                if is_bot_playing is False:
                                    is_bot_playing = True
                                    try:
                                        fulldir = player.duration
                                        minutes = str(int((fulldir / 60) % 60))
                                        seconds = str(int(fulldir % 60))
                                        if len(seconds) == 1:
                                            seconds = "0" + seconds
                                        track_info = str(botmessages['auto_playlist_data'][1]).format(
                                            str(player.title),
                                            str(player.uploader))
                                        message_data = str(botmessages['auto_playlist_data'][2]).format(
                                            track_info, minutes, seconds)
                                        yield from client.send_message(voice_message_channel, message_data)
                                        try:
                                            bot_playlist_entries.remove(track_info)
                                        except ValueError:
                                            pass
                                    except discord.errors.Forbidden:
                                        yield from BotPMError.resolve_send_message_error(client, message)
                                    if player is not None:
                                        player.start()
                        except UnboundLocalError:
                            is_bot_playing = False
        if message.content.startswith(_bot_prefix + 'LeaveVoiceChannel'):
            if message.author.id in banlist['Users']:
                return
            elif voice is not None:
                if voice_message_channel is not None:
                    if message.channel.id == voice_message_channel.id:
                        try:
                            yield from voice.disconnect()
                        except ConnectionResetError:
                            # Supress a Error here.
                            pass
                        if vchannel is not None:
                            try:
                                botvoicechannel['Bot_Current_Voice_Channel'].remove(vchannel.id)
                            except ValueError:
                                pass
                            try:
                                botvoicechannel['Bot_Current_Voice_Channel'].remove(voice_message_server.id)
                            except ValueError:
                                pass
                            try:
                                botvoicechannel['Bot_Current_Voice_Channel'].remove(voice_message_channel.id)
                            except ValueError:
                                pass
                            try:
                                botvoicechannel['Bot_Current_Voice_Channel'].remove(voice_message_server_name)
                            except ValueError:
                                pass
                            try:
                                botvoicechannel['Bot_Current_Voice_Channel'].remove(vchannel_name)
                            except ValueError:
                                pass
                        filename = "{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json".format(sys.path[0], sepa)
                        json.dump(botvoicechannel, open(filename, "w"))
                        try:
                            try:
                                message_data = str(botmessages['leave_voice_channel_command_data'][0]).format(
                                    vchannel.name)
                            except AttributeError:
                                message_data = str(botmessages['leave_voice_channel_command_data'][0]).format(
                                    vchannel_name)
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                        vchannel = None
                        voice_message_channel = None
                        voice = None
                        vchannel_name = None
                        if player is not None:
                            player = None
                        voice_message_server = None
                        if is_bot_playing is True:
                            is_bot_playing = False
                    else:
                        return
            else:
                msgdata = str(botmessages['leave_voice_channel_command_data'][1])
                message_data = msgdata
                yield from client.send_message(message.channel, message_data)
        if message.content.startswith(_bot_prefix + 'Playlist'):
            track1 = str(botmessages['playlist_command_data'][0])
            track2 = str(botmessages['playlist_command_data'][0])
            track3 = str(botmessages['playlist_command_data'][0])
            track4 = str(botmessages['playlist_command_data'][0])
            track5 = str(botmessages['playlist_command_data'][0])
            track6 = str(botmessages['playlist_command_data'][0])
            track7 = str(botmessages['playlist_command_data'][0])
            track8 = str(botmessages['playlist_command_data'][0])
            track9 = str(botmessages['playlist_command_data'][0])
            track10 = str(botmessages['playlist_command_data'][0])
            if message.author.id in banlist['Users']:
                return
            elif len(bot_playlist_entries) == 0:
                track1 = str(botmessages['playlist_command_data'][0])
                track2 = str(botmessages['playlist_command_data'][0])
                track3 = str(botmessages['playlist_command_data'][0])
                track4 = str(botmessages['playlist_command_data'][0])
                track5 = str(botmessages['playlist_command_data'][0])
                track6 = str(botmessages['playlist_command_data'][0])
                track7 = str(botmessages['playlist_command_data'][0])
                track8 = str(botmessages['playlist_command_data'][0])
                track9 = str(botmessages['playlist_command_data'][0])
                track10 = str(botmessages['playlist_command_data'][0])
            elif len(bot_playlist_entries) == 1:
                track1 = str(bot_playlist_entries[0])
                track2 = str(botmessages['playlist_command_data'][0])
                track3 = str(botmessages['playlist_command_data'][0])
                track4 = str(botmessages['playlist_command_data'][0])
                track5 = str(botmessages['playlist_command_data'][0])
                track6 = str(botmessages['playlist_command_data'][0])
                track7 = str(botmessages['playlist_command_data'][0])
                track8 = str(botmessages['playlist_command_data'][0])
                track9 = str(botmessages['playlist_command_data'][0])
                track10 = str(botmessages['playlist_command_data'][0])
            elif len(bot_playlist_entries) == 2:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(botmessages['playlist_command_data'][0])
                track4 = str(botmessages['playlist_command_data'][0])
                track5 = str(botmessages['playlist_command_data'][0])
                track6 = str(botmessages['playlist_command_data'][0])
                track7 = str(botmessages['playlist_command_data'][0])
                track8 = str(botmessages['playlist_command_data'][0])
                track9 = str(botmessages['playlist_command_data'][0])
                track10 = str(botmessages['playlist_command_data'][0])
            elif len(bot_playlist_entries) == 3:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(botmessages['playlist_command_data'][0])
                track5 = str(botmessages['playlist_command_data'][0])
                track6 = str(botmessages['playlist_command_data'][0])
                track7 = str(botmessages['playlist_command_data'][0])
                track8 = str(botmessages['playlist_command_data'][0])
                track9 = str(botmessages['playlist_command_data'][0])
                track10 = str(botmessages['playlist_command_data'][0])
            elif len(bot_playlist_entries) == 4:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(botmessages['playlist_command_data'][0])
                track6 = str(botmessages['playlist_command_data'][0])
                track7 = str(botmessages['playlist_command_data'][0])
                track8 = str(botmessages['playlist_command_data'][0])
                track9 = str(botmessages['playlist_command_data'][0])
                track10 = str(botmessages['playlist_command_data'][0])
            elif len(bot_playlist_entries) == 5:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(bot_playlist_entries[4])
                track6 = str(botmessages['playlist_command_data'][0])
                track7 = str(botmessages['playlist_command_data'][0])
                track8 = str(botmessages['playlist_command_data'][0])
                track9 = str(botmessages['playlist_command_data'][0])
                track10 = str(botmessages['playlist_command_data'][0])
            elif len(bot_playlist_entries) == 6:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(bot_playlist_entries[4])
                track6 = str(bot_playlist_entries[5])
                track7 = str(botmessages['playlist_command_data'][0])
                track8 = str(botmessages['playlist_command_data'][0])
                track9 = str(botmessages['playlist_command_data'][0])
                track10 = str(botmessages['playlist_command_data'][0])
            elif len(bot_playlist_entries) == 7:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(bot_playlist_entries[4])
                track6 = str(bot_playlist_entries[5])
                track7 = str(bot_playlist_entries[6])
                track8 = str(botmessages['playlist_command_data'][0])
                track9 = str(botmessages['playlist_command_data'][0])
                track10 = str(botmessages['playlist_command_data'][0])
            elif len(bot_playlist_entries) == 8:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(bot_playlist_entries[4])
                track6 = str(bot_playlist_entries[5])
                track7 = str(bot_playlist_entries[6])
                track8 = str(bot_playlist_entries[7])
                track9 = str(botmessages['playlist_command_data'][0])
                track10 = str(botmessages['playlist_command_data'][0])
            elif len(bot_playlist_entries) == 9:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(bot_playlist_entries[4])
                track6 = str(bot_playlist_entries[5])
                track7 = str(bot_playlist_entries[6])
                track8 = str(bot_playlist_entries[7])
                track9 = str(bot_playlist_entries[8])
                track10 = str(botmessages['playlist_command_data'][0])
            elif len(bot_playlist_entries) == 10:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(bot_playlist_entries[4])
                track6 = str(bot_playlist_entries[5])
                track7 = str(bot_playlist_entries[6])
                track8 = str(bot_playlist_entries[7])
                track9 = str(bot_playlist_entries[8])
                track10 = str(bot_playlist_entries[9])
            msgdata = str(botmessages['playlist_command_data'][1]).format(track1, track2, track3, track4, track5,
                                                                          track6, track7, track8, track9, track10)
            message_data = msgdata
            yield from client.send_message(message.channel, message_data)
        if message.content.startswith(_bot_prefix + "vol"):
            if message.author.id in banlist['Users']:
                return
            elif voice_message_channel is not None:
                if message.channel.id == voice_message_channel.id:
                    if player is not None:
                        value_string = message.content.strip(_bot_prefix + "vol ")
                        try:
                            value = int(value_string) / 100
                            if 0.0 <= value <= 2.0:
                                player.volume = value
                                value_message = str(botmessages['volume_command_data'][0]).format(str(value * 100))
                                yield from client.send_message(voice_message_channel, value_message)
                            else:
                                yield from client.send_message(voice_message_channel,
                                                               str(botmessages['volume_command_data'][1]))
                        except ValueError:
                            yield from client.send_message(voice_message_channel,
                                                           str(botmessages['volume_command_data'][2]))
                else:
                    yield from client.send_message(voice_message_channel, str(botmessages['volume_command_data'][3]))

    @asyncio.coroutine
    def voice_stuff_new_disabled_code(self, client, message):
        """
            :rtype: Message object
            :param client: Discord.py Client Object
            :param message: Message Object
        """
        if message.content.startswith(_bot_prefix + 'JoinVoiceChannel'):
            msgdata = str(botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'play'):
            msgdata = str(botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'stop'):
            msgdata = str(botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'pause'):
            msgdata = str(botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'unpause'):
            msgdata = str(botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'move'):
            msgdata = str(botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'LeaveVoiceChannel'):
            msgdata = str(botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'Playlist'):
            msgdata = str(botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + "vol"):
            msgdata = str(botmessages['voice_commands_disabled'][0])
            yield from client.send_message(message.channel, msgdata)

    @asyncio.coroutine
    def reload_commands_bypass1_new_code(self, client, message, reload_reason):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Message.
        :param reload_reason: Reason for reloading.
        :return: Nothing.
        """
        global player
        global vchannel
        global ffmout
        global vchannel_name
        global voice_message_channel
        global voice
        global _sent_finished_message
        global voice_message_server
        global is_bot_playing
        global voice_message_server_name
        ffmout.close()
        if voice is not None:
            yield from voice.disconnect()
            if voice_message_channel is not None:
                try:
                    if reload_reason is not None:
                        try:
                            message_data = str(botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                vchannel.name, reload_reason)
                        except AttributeError:
                            message_data = str(botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                vchannel_name, reload_reason)
                    else:
                        reason = str(botmessages['reload_commands_voice_channels_bypass1'][1])
                        try:
                            message_data = str(botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                vchannel.name, reason)
                        except AttributeError:
                            message_data = str(botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                vchannel_name, reason)
                    yield from client.send_message(voice_message_channel, message_data)
                    voice_message_channel = None
                    voice = None
                    vchannel = None
                    voice_message_server = None
                    player = None
                    vchannel_name = None
                    _sent_finished_message = False
                    voice_message_server_name = None
                    is_bot_playing = False
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def reload_commands_bypass2_new_code(self, client, message):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        global vchannel
        global voice
        global voice_message_server
        global voice_message_channel
        global voice_message_server_name
        global vchannel_name
        global verror
        botvoicechannel_reloaded = None
        try:
            botvoicechannelfile = io.open('{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json'.format(sys.path[0],
                                                                                                       sepa))
            botvoicechannel_reloaded = json.load(botvoicechannelfile)
            botvoicechannelfile.close()
        except FileNotFoundError:
            pass
        try:
            vchannel_2 = str(botvoicechannel_reloaded['Bot_Current_Voice_Channel'][0])
            vmserver = str(botvoicechannel_reloaded['Bot_Current_Voice_Channel'][1])
            vmchannel = str(botvoicechannel_reloaded['Bot_Current_Voice_Channel'][2])
            voice_message_server_name = str(botvoicechannel_reloaded['Bot_Current_Voice_Channel'][3])
            vchannel_name = str(botvoicechannel_reloaded['Bot_Current_Voice_Channel'][4])
            vchannel = discord.Object(id=vchannel_2)
            voice_message_server = discord.Object(id=vmserver)
            voice_message_channel = discord.Object(id=vmchannel)
            try:
                voice = yield from client.join_voice_channel(vchannel)
                verror = False
            except discord.errors.ConnectionClosed:
                pass
            except discord.errors.InvalidArgument:
                voice_message_server_name = None
                vchannel_name = None
                vchannel = None
                voice_message_server = None
                voice_message_channel = None
                voice = None
                verror = True
            except concurrent.futures._base.TimeoutError:
                yield from client.send_message(message.channel,
                                               str(botmessages['reload_commands_voice_channels_bypass2'][0]))
                voice_message_server_name = None
                vchannel_name = None
                vchannel = None
                voice_message_server = None
                voice_message_channel = None
                voice = None
                verror = True
            except RuntimeError:
                voice_message_server_name = None
                vchannel_name = None
                vchannel = None
                voice_message_server = None
                voice_message_channel = None
                voice = None
                verror = True
                msgdata = str(botmessages['reload_commands_voice_channels_bypass2'][1])
                yield from client.send_message(voice_message_channel, msgdata)
            if verror is not True:
                message_data = str(botmessages['reload_commands_voice_channels_bypass2'][2]).format(vchannel_name)
                yield from client.send_message(voice_message_channel, message_data)
        except IndexError:
            voice_message_server_name = None
            vchannel_name = None
            vchannel = None
            voice_message_server = None
            voice_message_channel = None
            voice = None

    @asyncio.coroutine
    def reload_commands_bypass3_new_code(self, client):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :return: Nothing.
        """
        global vchannel
        global voice
        global voice_message_server
        global voice_message_channel
        global voice_message_server_name
        global vchannel_name
        global verror
        try:
            vchannel_2 = str(botvoicechannel['Bot_Current_Voice_Channel'][0])
            vmserver = str(botvoicechannel['Bot_Current_Voice_Channel'][1])
            vmchannel = str(botvoicechannel['Bot_Current_Voice_Channel'][2])
            voice_message_server_name = str(botvoicechannel['Bot_Current_Voice_Channel'][3])
            vchannel_name = str(botvoicechannel['Bot_Current_Voice_Channel'][4])
            vchannel = discord.Object(id=vchannel_2)
            voice_message_server = discord.Object(id=vmserver)
            voice_message_channel = discord.Object(id=vmchannel)
            discord.opus.load_opus(opusdll)
            try:
                voice = yield from client.join_voice_channel(vchannel)
                verror = False
            except discord.errors.ConnectionClosed:
                pass
            except discord.errors.InvalidArgument:
                voice_message_server_name = None
                vchannel_name = None
                vchannel = None
                voice_message_server = None
                voice_message_channel = None
                voice = None
                verror = True
            except RuntimeError:
                voice_message_server_name = None
                vchannel_name = None
                vchannel = None
                voice_message_server = None
                voice_message_channel = None
                voice = None
                verror = True
                msgdata = str(botmessages['reload_commands_voice_channels_bypass2'][1])
                yield from client.send_message(voice_message_channel, msgdata)
            if verror is not True:
                message_data = str(botmessages['reload_commands_voice_channels_bypass2'][2]).format(vchannel_name)
                yield from client.send_message(voice_message_channel, message_data)
        except IndexError:
            voice_message_server_name = None
            vchannel_name = None
            vchannel = None
            voice_message_server = None
            voice_message_channel = None
            voice = None

    @asyncio.coroutine
    def reload_commands_bypass4_new_code(self, client, message, reload_reason):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Message.
        :param reload_reason: Reason for reloading.
        :return: Nothing.
        """
        global player
        global vchannel
        global vchannel_name
        global voice_message_channel
        global voice
        global _sent_finished_message
        global voice_message_server
        global is_bot_playing
        global voice_message_server_name
        if voice is not None:
            yield from voice.disconnect()
            if voice_message_channel is not None:
                try:
                    if reload_reason is not None:
                        try:
                            message_data = str(botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                vchannel.name, reload_reason)
                        except AttributeError:
                            message_data = str(botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                vchannel_name, reload_reason)
                    else:
                        reason = str(botmessages['reload_commands_voice_channels_bypass4'][0])
                        try:
                            message_data = str(botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                vchannel.name, reason)
                        except AttributeError:
                            message_data = str(botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                vchannel_name, reason)
                    yield from client.send_message(voice_message_channel, message_data)
                    voice_message_channel = None
                    voice = None
                    vchannel = None
                    voice_message_server = None
                    player = None
                    vchannel_name = None
                    _sent_finished_message = False
                    voice_message_server_name = None
                    is_bot_playing = False
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)


class VoiceBotCommands:
    """
    Class for Voice Channel Functionality in this bot.
    """
    def __init__(self):
        self.bot = BotData()

    @asyncio.coroutine
    def voice_stuff_new(self, client, message):
        """
        Listens for the Voice Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.voice_stuff_new_code(client, message)

    @asyncio.coroutine
    def voice_stuff_new_disabled(self, client, message):
        """
        This is a Dummy function for disabling Voice channel stuffs when Discord.py has disconnect bugs.

        I am sorry for Any Inconvience however these bugs are because of Rapptz's Discord.py.

        To shut PyCharm the fuck up below.
        :param client:
        :param message:
        """
        yield from self.bot.voice_stuff_new_disabled_code(client, message)

    @asyncio.coroutine
    def reload_commands_bypass1_new(self, client, message, reload_reason):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Message.
        :param reload_reason: Reason for reloading.
        :return: Nothing.
        """
        yield from self.bot.reload_commands_bypass1_new_code(client, message, reload_reason)

    @asyncio.coroutine
    def reload_commands_bypass2_new(self, client, message):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.reload_commands_bypass2_new_code(client, message)

    @asyncio.coroutine
    def reload_commands_bypass3_new(self, client):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :return: Nothing.
        """
        yield from self.bot.reload_commands_bypass3_new_code(client)

    @asyncio.coroutine
    def reload_commands_bypass4_new(self, client, message, reload_reason):
        """
        Reloading Command Bypass for Voice Channels.
        :param client: Discord Client.
        :param message: Message.
        :param reload_reason: Reason for reloading.
        :return: Nothing.
        """
        yield from self.bot.reload_commands_bypass4_new_code(client, message, reload_reason)
