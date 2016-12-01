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
import discord
from discord.ext import commands
import json
import io
import sys
import os
import os.path
import youtube_dl
import ctypes
from .. import BotErrors
try:
    from .. import BotPMError
except ImportError:
    print('Some Unknown thing happened which made a critical bot code file unable to be found.')
    BotPMError = None
from .. import BotConfigReader
from sasync import *
import asyncio


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
        self.path = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(self.path, self.sepa)
        if os.path.isfile(self.path) and os.access(self.path, os.R_OK):
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


class VoiceBotCommands:
    """
    Class for Voice Channel Functionality in this bot.
    """
    def __init__(self, bot):
        self.bot = bot
        if self.bot.path.find('\\AppData\\Local\\Temp') != -1:
            self.bot.path = sys.executable.strip(
                'DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(self.bot.platform, sys.platform,
                                                                                       sys.implementation,
                                                                                       sys.version_info))
        if self.bot.bits == 4:
            if not (sys.platform.startswith('linux')):
                self.opusdll = '{0}{1}resources{1}opus{1}win32{1}{2}{1}opus.dll'.format(self.bot.path, self.bot.sepa,
                                                                                        self.bot.platform)
                os.chdir('{0}{1}resources{1}ffmpeg{1}win32{1}{2}'.format(self.bot.path, self.bot.sepa,
                                                                         self.bot.platform))
            else:
                self.opusdll = '{0}{1}resources{1}opus{1}linux{1}{2}{1}opus.dll'.format(self.bot.path, self.bot.sepa,
                                                                                        self.bot.platform)
                os.chdir('{0}{1}resources{1}ffmpeg{1}linux{1}{2}'.format(self.bot.path, self.bot.sepa,
                                                                         self.bot.platform))
        elif self.bot.bits == 8:
            if not (sys.platform.startswith('linux')):
                self.opusdll = '{0}{1}resources{1}opus{1}win32{1}{2}{1}opus.dll'.format(self.bot.path, self.bot.sepa,
                                                                                        self.bot.platform)
                os.chdir('{0}{1}resources{1}ffmpeg{1}win32{1}{2}'.format(self.bot.path, self.bot.sepa,
                                                                         self.bot.platform))
            else:
                self.opusdll = '{0}{1}resources{1}opus{1}linux{1}{2}{1}opus.dll'.format(self.bot.path, self.bot.sepa,
                                                                                        self.bot.platform)
                os.chdir('{0}{1}resources{1}ffmpeg{1}linux{1}{2}'.format(self.bot.path, self.bot.sepa,
                                                                         self.bot.platform))
        try:
            self.botvoicechannelfile = io.open(
                '{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json'.format(self.bot.path,
                                                                             self.bot.sepa))
            self.botvoicechannel = json.load(self.botvoicechannelfile)
            self.botvoicechannelfile.close()
        except FileNotFoundError:
            pass
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

    def setup(self):
        """
        Allows bot to rejoin voice channel when reloading.
        :return: Nothing.
        """
        self.bot.loop.create_task(self.__load())

    @async
    def __load(self):
        """
        Makes bot able to join a voice channel when the commands are loaded.
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
                self.voice = yield from self.bot.join_voice_channel(self.vchannel)
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
                yield from self.bot.send_message(self.voice_message_channel,
                                                 content=str(
                                                     self.bot.botmessages['reload_commands_voice_channels_bypass2'][0]))
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
                self.voice = None
                self.verror = True
                msgdata = str(self.bot.botmessages['reload_commands_voice_channels_bypass2'][1])
                yield from self.bot.send_message(self.voice_message_channel, content=msgdata)
                self.voice_message_channel = None
            if self.verror is not True:
                message_data = str(self.bot.botmessages['reload_commands_voice_channels_bypass2'][2]).format(
                    self.vchannel_name)
                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
        except IndexError:
            self.voice_message_server_name = None
            self.vchannel_name = None
            self.vchannel = None
            self.voice_message_server = None
            self.voice_message_channel = None
            self.voice = None
        except discord.errors.ClientException:
            pass  # already in a voice channel so lots not set those values to None.

    @async
    def __unload(self):
        """
        Makes bot able to leave Voice channel when reloading or unloading voice commands.
        """
        yield from self.__reload()

    @async
    def __reload(self):
        """
        Makes bot able to leave Voice channel when reloading or unloading voice commands.
        """
        try:
            if self.voice is not None:
                yield from self.voice.disconnect()
                if self.voice_message_channel is not None:
                    try:
                        reason = str(self.bot.botmessages['reload_commands_voice_channels_bypass1'][1])
                        try:
                            message_data = str(
                                self.bot.botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                self.vchannel.name, reason)
                        except AttributeError:
                            message_data = str(
                                self.bot.botmessages['reload_commands_voice_channels_bypass1'][0]).format(
                                self.vchannel_name, reason)
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
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
                        pass
        except Exception as e:
            str(e)
            pass

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
    def on_ready(self):
        """
        When Bot is ready.
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
                self.voice = yield from self.bot.join_voice_channel(self.vchannel)
                self.verror = False
            except discord.errors.ConnectionClosed:
                pass
            # except discord.errors.InvalidServerError:
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
                msgdata = str(self.bot.botmessages['reload_commands_voice_channels_bypass2'][1])
                yield from self.bot.send_message(self.voice_message_channel, content=msgdata)
            if self.verror is not True:
                message_data = str(self.bot.botmessages['reload_commands_voice_channels_bypass2'][2]).format(
                    self.vchannel_name)
                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                self.lock_join_voice_channel_command = False
        except IndexError:
            self.voice_message_server_name = None
            self.vchannel_name = None
            self.vchannel = None
            self.voice_message_server = None
            self.voice_message_channel = None
            self.voice = None
            self.lock_join_voice_channel_command = False

    @commands.command(name='JoinVoiceChannel', pass_context=True, no_pm=True)
    @async
    def join_voice_channel_command(self, ctx):
        """
        Bot Voice Command.
        :param ctx: Command Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        elif self.vchannel is not None:
            try:
                messagedata = str(self.bot.botmessages['join_voice_channel_command_data'][0])
                try:
                    message_data = messagedata.format(self.voice_message_server.name)
                except AttributeError:
                    message_data = messagedata.format(self.voice_message_server_name)
                yield from self.bot.send_message(ctx.message.channel, content=message_data)
            except discord.errors.Forbidden:
                yield from BotPMError.resolve_send_message_error(self.bot, ctx)
        else:
            if not self.lock_join_voice_channel_command:
                discord.opus.load_opus(self.opusdll)
                self.voice_message_channel = ctx.message.channel
                self.voice_message_server = ctx.message.channel.server
                self.voice_message_server_name = ctx.message.channel.server.name
                if ctx.message.author.voice_channel is not None:
                    self.vchannel = ctx.message.author.voice_channel
                    self.vchannel_name = ctx.message.author.voice_channel.name
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
                    file_name = "{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json".format(self.bot.path,
                                                                                             self.bot.sepa)
                    json.dump(self.botvoicechannel, open(file_name, "w"))
                    try:
                        try:
                            self.voice = yield from self.bot.join_voice_channel(self.vchannel)
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
                            msgdata = str(self.bot.botmessages['join_voice_channel_command_data'][6])
                            yield from self.bot.send_message(self.voice_message_channel, content=msgdata)
                        if not self.verror:
                            try:
                                msg_data = str(self.bot.botmessages['join_voice_channel_command_data'][1]).format(
                                    self.vchannel_name)
                                yield from self.bot.send_message(ctx.message.channel, content=msg_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                    except discord.errors.InvalidArgument:
                        self.voice_message_channel = None
                        self.voice = None
                        self.vchannel = None
                        self.voice_message_server = None
                        self.voice_message_server_name = None
                        self.vchannel_name = None
                        try:
                            msg_data = str(self.bot.botmessages['join_voice_channel_command_data'][2])
                            yield from self.bot.send_message(ctx.message.channel, content=msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                    except asyncio.TimeoutError:
                        self.voice_message_channel = None
                        self.voice = None
                        self.vchannel = None
                        self.voice_message_server = None
                        self.voice_message_server_name = None
                        self.vchannel_name = None
                        try:
                            msg_data = str(self.bot.botmessages['join_voice_channel_command_data'][3])
                            yield from self.bot.send_message(ctx.message.channel, content=msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                    except BotErrors.CommandTimeoutError:
                        yield from self.bot.send_message(
                            self.voice_message_channel, content=str(
                                self.bot.botmessages['reload_commands_voice_channels_bypass2'][0]))
                        self.voice_message_server_name = None
                        self.vchannel_name = None
                        self.vchannel = None
                        self.voice_message_server = None
                        self.voice_message_channel = None
                        self.voice = None
                        self.verror = True
                    except discord.errors.HTTPException:
                        self.voice_message_channel = None
                        self.voice = None
                        self.vchannel = None
                        self.voice_message_server = None
                        try:
                            msg_data = str(self.bot.botmessages['join_voice_channel_command_data'][4])
                            yield from self.bot.send_message(ctx.message.channel, content=msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                    except discord.opus.OpusNotLoaded:
                        self.voice_message_channel = None
                        self.voice = None
                        self.vchannel = None
                        self.voice_message_server = None
                        self.voice_message_server_name = None
                        self.vchannel_name = None
                        try:
                            msg_data = str(self.bot.botmessages['join_voice_channel_command_data'][5])
                            yield from self.bot.send_message(ctx.message.channel, content=msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                    except IndexError:
                        return

    @commands.command(name='play', pass_context=True, no_pm=True)
    @async
    def play_command(self, ctx):
        """
        Bot Voice Command.
        :param ctx: Command Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        elif self.is_bot_playing is False:
            if self.voice is not None:
                if self.voice_message_channel is not None:
                    if ctx.message.channel.id == self.voice_message_channel.id:
                        try:
                            data = ctx.message.content[len(self.bot.bot_prefix + "play "):].strip()
                            if data == "":
                                try:
                                    message_data = str(self.bot.botmessages['play_command_data'][0])
                                    yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(self.bot, ctx.message)
                            if data.rfind('https://') == -1 and data.rfind('http://') == -1:
                                # lets try to do a search.
                                self.player = yield from self.voice.create_ytdl_player(data,
                                                                                       ytdl_options=self.ytdlo,
                                                                                       options=self.ffmop,
                                                                                       after=self.voice_playlist)
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
                                            message_data = str(self.bot.botmessages['play_command_data'][1]).format(
                                                str(self.player.title), str(self.player.uploader), minutes, seconds)
                                            yield from self.bot.send_message(self.voice_message_channel,
                                                                             content=message_data)
                                        except discord.errors.Forbidden:
                                            yield from BotPMError.resolve_send_message_error(self.bot, ctx.message)
                                        try:
                                            self.player.start()
                                        except RuntimeError:
                                            pass
                                    except AttributeError:
                                        message_data = str(self.bot.botmessages['play_command_data'][2])
                                        self.is_bot_playing = False
                                        yield from self.bot.send_message(self.voice_message_channel,
                                                                         content=message_data)
                            else:
                                if '<' and '>' in data:
                                    data = data.strip('<')
                                    data = data.strip('>')
                                if 'www.youtube.com/watch?v=' in data or 'soundcloud.com' in data:
                                    self.player = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop,
                                                                                           after=self.voice_playlist)
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
                                                message_data = str(self.bot.botmessages['play_command_data'][1]).format(
                                                    str(self.player.title), str(self.player.uploader), minutes,
                                                    seconds)
                                                yield from self.bot.send_message(self.voice_message_channel,
                                                                                 content=message_data)
                                            except discord.errors.Forbidden:
                                                yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                                            try:
                                                self.player.start()
                                            except RuntimeError:
                                                pass
                                        except AttributeError:
                                            message_data = str(self.bot.botmessages['play_command_data'][2])
                                            self.is_bot_playing = False
                                            yield from self.bot.send_message(self.voice_message_channel,
                                                                             content=message_data)
                        except IndexError:
                            return
                        except discord.errors.HTTPException:
                            message_data = str(self.bot.botmessages['play_command_data'][4]).format(str(sys.path))
                            yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            self.player = None
                        except youtube_dl.utils.UnsupportedError:
                            yield from self.bot.send_message(ctx.message.channel,
                                                             content=str(self.bot.botmessages['play_command_data'][5]))
                            self.player = None
                        except youtube_dl.utils.ExtractorError:
                            message_data = str(self.bot.botmessages['play_command_data'][6])
                            yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            self.player = None
                        except youtube_dl.utils.DownloadError:
                            yield from self.bot.send_message(ctx.message.channel,
                                                             content=str(self.bot.botmessages['play_command_data'][7]))
                            self.player = None
                    else:
                        return
            else:
                message_data = str(self.bot.botmessages['play_command_data'][8])
                yield from self.bot.send_message(ctx.message.channel, content=message_data)
        else:
            if self.player is not None:
                data = ctx.message.content[len(self.bot.bot_prefix + "play "):].strip()
                if data == "":
                    try:
                        message_data = str(self.bot.botmessages['play_command_data'][9])
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
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
                                track1 = str(self.bot.botmessages['play_command_data'][10]).format(playlist01)
                                fulldir = playlist01time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track1time = newdir
                                track1uploader = str(self._temp_player_1.uploader)
                                track1info = str(self.bot.botmessages['play_command_data'][12]).format(track1,
                                                                                                       track1uploader,
                                                                                                       track1time)
                                self.bot_playlist_entries.append(track1info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track1, track1time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif data in self.bot_playlist:
                            msgdata = str(self.bot.botmessages['play_command_data'][14])
                            message_data = msgdata
                            yield from self.bot.send_message(ctx.message.channel, content=message_data)
                        elif len(self.bot_playlist) == 1:
                            self._temp_player_2 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist02 = self._temp_player_2.title
                                playlist02time = self._temp_player_2.duration
                                track2 = str(self.bot.botmessages['play_command_data'][10]).format(playlist02)
                                fulldir = playlist02time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track2time = newdir
                                track2uploader = str(self._temp_player_2.uploader)
                                track2info = str(self.bot.botmessages['play_command_data'][12]).format(track2,
                                                                                                       track2uploader,
                                                                                                       track2time)
                                self.bot_playlist_entries.append(track2info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track2, track2time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 2:
                            self._temp_player_3 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist03 = self._temp_player_3.title
                                playlist03time = self._temp_player_3.duration
                                track3 = str(self.bot.botmessages['play_command_data'][10]).format(playlist03)
                                fulldir = playlist03time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track3time = newdir
                                track3uploader = str(self._temp_player_3.uploader)
                                track3info = str(self.bot.botmessages['play_command_data'][12]).format(track3,
                                                                                                       track3uploader,
                                                                                                       track3time)
                                self.bot_playlist_entries.append(track3info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track3, track3time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 3:
                            self._temp_player_4 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist04 = self._temp_player_4.title
                                playlist04time = self._temp_player_4.duration
                                track4 = str(self.bot.botmessages['play_command_data'][10]).format(playlist04)
                                fulldir = playlist04time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track4time = newdir
                                track4uploader = str(self._temp_player_4.uploader)
                                track4info = str(self.bot.botmessages['play_command_data'][12]).format(track4,
                                                                                                       track4uploader,
                                                                                                       track4time)
                                self.bot_playlist_entries.append(track4info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track4, track4time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 4:
                            self._temp_player_5 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist05 = self._temp_player_5.title
                                playlist05time = self._temp_player_5.duration
                                track5 = str(self.bot.botmessages['play_command_data'][10]).format(playlist05)
                                fulldir = playlist05time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track5time = newdir
                                track5uploader = str(self._temp_player_5.uploader)
                                track5info = str(self.bot.botmessages['play_command_data'][12]).format(track5,
                                                                                                       track5uploader,
                                                                                                       track5time)
                                self.bot_playlist_entries.append(track5info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track5, track5time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 5:
                            self._temp_player_6 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist06 = self._temp_player_6.title
                                playlist06time = self._temp_player_6.duration
                                track6 = str(self.bot.botmessages['play_command_data'][10]).format(playlist06)
                                fulldir = playlist06time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track6time = newdir
                                track6uploader = str(self._temp_player_6.uploader)
                                track6info = str(self.bot.botmessages['play_command_data'][12]).format(track6,
                                                                                                       track6uploader,
                                                                                                       track6time)
                                self.bot_playlist_entries.append(track6info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track6, track6time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 6:
                            self._temp_player_7 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist07 = self._temp_player_7.title
                                playlist07time = self._temp_player_7.duration
                                track7 = str(self.bot.botmessages['play_command_data'][10]).format(playlist07)
                                fulldir = playlist07time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track7time = newdir
                                track7uploader = str(self._temp_player_7.uploader)
                                track7info = str(self.bot.botmessages['play_command_data'][12]).format(track7,
                                                                                                       track7uploader,
                                                                                                       track7time)
                                self.bot_playlist_entries.append(track7info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track7, track7time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 7:
                            self._temp_player_8 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist08 = self._temp_player_8.title
                                playlist08time = self._temp_player_8.duration
                                track8 = str(self.bot.botmessages['play_command_data'][10]).format(playlist08)
                                fulldir = playlist08time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track8time = newdir
                                track8uploader = str(self._temp_player_8.uploader)
                                track8info = str(self.bot.botmessages['play_command_data'][12]).format(track8,
                                                                                                       track8uploader,
                                                                                                       track8time)
                                self.bot_playlist_entries.append(track8info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track8, track8time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 8:
                            self._temp_player_9 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist09 = self._temp_player_9.title
                                playlist09time = self._temp_player_9.duration
                                track9 = str(self.bot.botmessages['play_command_data'][10]).format(playlist09)
                                fulldir = playlist09time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track9time = newdir
                                track9uploader = str(self._temp_player_9.uploader)
                                track9info = str(self.bot.botmessages['play_command_data'][12]).format(track9,
                                                                                                       track9uploader,
                                                                                                       track9time)
                                self.bot_playlist_entries.append(track9info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track9, track9time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 9:
                            self._temp_player_10 = yield from self.voice.create_ytdl_player(data,
                                                                                            ytdl_options=self.ytdlo,
                                                                                            options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist10 = self._temp_player_10.title
                                playlist10time = self._temp_player_10.duration
                                track10 = str(self.bot.botmessages['play_command_data'][10]).format(playlist10)
                                fulldir = playlist10time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track10time = newdir
                                track10uploader = str(self._temp_player_10.uploader)
                                track10info = str(self.bot.botmessages['play_command_data'][12]).format(track10,
                                                                                                        track10uploader,
                                                                                                        track10time)
                                self.bot_playlist_entries.append(track10info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track10,
                                                                                                    track10time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 10:
                            msgdata = str(self.bot.botmessages['play_command_data'][15])
                            message_data = msgdata
                            yield from self.bot.send_message(ctx.message.channel, content=message_data)
                    if 'www.youtube.com/watch?v=' in data or 'soundcloud.com' in data:
                        if len(self.bot_playlist) == 0:
                            self._temp_player_1 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist01 = self._temp_player_1.title
                                playlist01time = self._temp_player_1.duration
                                track1 = str(self.bot.botmessages['play_command_data'][10]).format(playlist01)
                                fulldir = playlist01time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track1time = newdir
                                track1uploader = str(self._temp_player_1.uploader)
                                track1info = str(self.bot.botmessages['play_command_data'][12]).format(track1,
                                                                                                       track1uploader,
                                                                                                       track1time)
                                self.bot_playlist_entries.append(track1info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track1, track1time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif data in self.bot_playlist:
                            msgdata = str(self.bot.botmessages['play_command_data'][14])
                            message_data = msgdata
                            yield from self.bot.send_message(ctx.message.channel, content=message_data)
                        elif len(self.bot_playlist) == 1:
                            self._temp_player_2 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist02 = self._temp_player_2.title
                                playlist02time = self._temp_player_2.duration
                                track2 = str(self.bot.botmessages['play_command_data'][10]).format(playlist02)
                                fulldir = playlist02time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track2time = newdir
                                track2uploader = str(self._temp_player_2.uploader)
                                track2info = str(self.bot.botmessages['play_command_data'][12]).format(track2,
                                                                                                       track2uploader,
                                                                                                       track2time)
                                self.bot_playlist_entries.append(track2info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track2, track2time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 2:
                            self._temp_player_3 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist03 = self._temp_player_3.title
                                playlist03time = self._temp_player_3.duration
                                track3 = str(self.bot.botmessages['play_command_data'][10]).format(playlist03)
                                fulldir = playlist03time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track3time = newdir
                                track3uploader = str(self._temp_player_3.uploader)
                                track3info = str(self.bot.botmessages['play_command_data'][12]).format(track3,
                                                                                                       track3uploader,
                                                                                                       track3time)
                                self.bot_playlist_entries.append(track3info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track3, track3time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 3:
                            self._temp_player_4 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist04 = self._temp_player_4.title
                                playlist04time = self._temp_player_4.duration
                                track4 = str(self.bot.botmessages['play_command_data'][10]).format(playlist04)
                                fulldir = playlist04time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track4time = newdir
                                track4uploader = str(self._temp_player_4.uploader)
                                track4info = str(self.bot.botmessages['play_command_data'][12]).format(track4,
                                                                                                       track4uploader,
                                                                                                       track4time)
                                self.bot_playlist_entries.append(track4info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track4, track4time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 4:
                            self._temp_player_5 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist05 = self._temp_player_5.title
                                playlist05time = self._temp_player_5.duration
                                track5 = str(self.bot.botmessages['play_command_data'][10]).format(playlist05)
                                fulldir = playlist05time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track5time = newdir
                                track5uploader = str(self._temp_player_5.uploader)
                                track5info = str(self.bot.botmessages['play_command_data'][12]).format(track5,
                                                                                                       track5uploader,
                                                                                                       track5time)
                                self.bot_playlist_entries.append(track5info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track5, track5time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 5:
                            self._temp_player_6 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist06 = self._temp_player_6.title
                                playlist06time = self._temp_player_6.duration
                                track6 = str(self.bot.botmessages['play_command_data'][10]).format(playlist06)
                                fulldir = playlist06time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track6time = newdir
                                track6uploader = str(self._temp_player_6.uploader)
                                track6info = str(self.bot.botmessages['play_command_data'][12]).format(track6,
                                                                                                       track6uploader,
                                                                                                       track6time)
                                self.bot_playlist_entries.append(track6info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track6, track6time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 6:
                            self._temp_player_7 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist07 = self._temp_player_7.title
                                playlist07time = self._temp_player_7.duration
                                track7 = str(self.bot.botmessages['play_command_data'][10]).format(playlist07)
                                fulldir = playlist07time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track7time = newdir
                                track7uploader = str(self._temp_player_7.uploader)
                                track7info = str(self.bot.botmessages['play_command_data'][12]).format(track7,
                                                                                                       track7uploader,
                                                                                                       track7time)
                                self.bot_playlist_entries.append(track7info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track7, track7time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 7:
                            self._temp_player_8 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist08 = self._temp_player_8.title
                                playlist08time = self._temp_player_8.duration
                                track8 = str(self.bot.botmessages['play_command_data'][10]).format(playlist08)
                                fulldir = playlist08time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track8time = newdir
                                track8uploader = str(self._temp_player_8.uploader)
                                track8info = str(self.bot.botmessages['play_command_data'][12]).format(track8,
                                                                                                       track8uploader,
                                                                                                       track8time)
                                self.bot_playlist_entries.append(track8info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track8, track8time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 8:
                            self._temp_player_9 = yield from self.voice.create_ytdl_player(data,
                                                                                           ytdl_options=self.ytdlo,
                                                                                           options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist09 = self._temp_player_9.title
                                playlist09time = self._temp_player_9.duration
                                track9 = str(self.bot.botmessages['play_command_data'][10]).format(playlist09)
                                fulldir = playlist09time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track9time = newdir
                                track9uploader = str(self._temp_player_9.uploader)
                                track9info = str(self.bot.botmessages['play_command_data'][12]).format(track9,
                                                                                                       track9uploader,
                                                                                                       track9time)
                                self.bot_playlist_entries.append(track9info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track9, track9time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 9:
                            self._temp_player_10 = yield from self.voice.create_ytdl_player(data,
                                                                                            ytdl_options=self.ytdlo,
                                                                                            options=self.ffmop)
                            self.bot_playlist.append(data)
                            try:
                                playlist10 = self._temp_player_10.title
                                playlist10time = self._temp_player_10.duration
                                track10 = str(self.bot.botmessages['play_command_data'][10]).format(playlist10)
                                fulldir = playlist10time
                                minutes = str(int((fulldir / 60) % 60))
                                seconds = str(int(fulldir % 60))
                                if len(seconds) == 1:
                                    seconds = "0" + seconds
                                newdir = str(self.bot.botmessages['play_command_data'][11]).format(minutes, seconds)
                                track10time = newdir
                                track10uploader = str(self._temp_player_10.uploader)
                                track10info = str(self.bot.botmessages['play_command_data'][12]).format(track10,
                                                                                                        track10uploader,
                                                                                                        track10time)
                                self.bot_playlist_entries.append(track10info)
                                msgdata = str(self.bot.botmessages['play_command_data'][13]).format(track10,
                                                                                                    track10time)
                                message_data = msgdata
                                yield from self.bot.send_message(ctx.message.channel, content=message_data)
                            except AttributeError:
                                message_data = str(self.bot.botmessages['play_command_data'][2])
                                yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        elif len(self.bot_playlist) == 10:
                            msgdata = str(self.bot.botmessages['play_command_data'][15])
                            message_data = msgdata
                            yield from self.bot.send_message(ctx.message.channel, content=message_data)

    @commands.command(name='stop', pass_context=True, no_pm=True)
    @async
    def stop_command(self, ctx):
        """
        Bot Voice Command.
        :param ctx: Command Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        elif self.voice_message_channel is not None:
            if ctx.message.channel.id == self.voice_message_channel.id:
                if self.player is not None:
                    fulldir = self.player.duration
                    minutes = str(int((fulldir / 60) % 60))
                    seconds = str(int(fulldir % 60))
                    if len(seconds) == 1:
                        seconds = "0" + seconds
                    try:
                        message_data = str(self.bot.botmessages['stop_command_data'][0]).format(str(self.player.title),
                                                                                                str(self.player.uploader
                                                                                                    ), minutes, seconds)
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
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
                                        track_info = str(self.bot.botmessages['stop_command_data'][1]).format(
                                            str(self.player.title),
                                            str(self.player.uploader))
                                        message_data = str(self.bot.botmessages['stop_command_data'][2]).format(
                                            track_info, minutes, seconds)
                                        yield from self.bot.send_message(self.voice_message_channel,
                                                                         content=message_data)
                                        try:
                                            self.bot_playlist_entries.remove(track_info)
                                        except ValueError:
                                            pass
                                    except discord.errors.Forbidden:
                                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                                    if self.player is not None:
                                        self.player.start()
                        except UnboundLocalError:
                            self.player = None
                            self.is_bot_playing = False
                else:
                    try:
                        message_data = str(self.bot.botmessages['stop_command_data'][3])
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
            else:
                return

    @commands.command(name='pause', pass_context=True, no_pm=True)
    @async
    def pause_command(self, ctx):
        """
        Bot Voice Command.
        :param ctx: Command Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        elif self.voice_message_channel is not None:
            if ctx.message.channel.id == self.voice_message_channel.id:
                if self.player is not None:
                    fulldir = self.player.duration
                    minutes = str(int((fulldir / 60) % 60))
                    seconds = str(int(fulldir % 60))
                    if len(seconds) == 1:
                        seconds = "0" + seconds
                    try:
                        message_data = str(self.bot.botmessages['pause_command_data'][0]).format(
                            str(self.player.title), str(self.player.uploader), minutes, seconds)
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                    self.player.pause()
                else:
                    message_data = str(self.bot.botmessages['pause_command_data'][1])
                    yield from self.bot.send_message(self.voice_message_channel, content=message_data)
            else:
                return
        else:
            message_data = str(self.bot.botmessages['pause_command_data'][2])
            yield from self.bot.send_message(ctx.message.channel, content=message_data)

    @commands.command(name='unpause', pass_context=True, no_pm=True)
    @async
    def unpause_command(self, ctx):
        """
        Bot Voice Command.
        :param ctx: Command Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        elif self.voice_message_channel is not None:
            if ctx.message.channel.id == self.voice_message_channel.id:
                if self.player is not None:
                    fulldir = self.player.duration
                    minutes = str(int((fulldir / 60) % 60))
                    seconds = str(int(fulldir % 60))
                    if len(seconds) == 1:
                        seconds = "0" + seconds
                    try:
                        message_data = str(self.bot.botmessages['unpause_command_data'][0]).format(
                            str(self.player.title), str(self.player.uploader), minutes, seconds)
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                    self.player.resume()
                else:
                    try:
                        msgdata = str(self.bot.botmessages['unpause_command_data'][1])
                        message_data = msgdata
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
            else:
                return
        else:
            message_data = str(self.bot.botmessages['unpause_command_data'][2])
            yield from self.bot.send_message(ctx.message.channel, content=message_data)

    @commands.command(name='move', pass_context=True, no_pm=True)
    @async
    def move_command(self, ctx):
        """
        Bot Voice Command.
        :param ctx: Command Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        elif self.voice_message_channel is not None:
            if ctx.message.channel.id == self.voice_message_channel.id:
                self.vchannel = ctx.message.author.voice_channel
                bot = ctx.message.channel.server.get_member_named('{0}#{1}'.format(self.bot.user.name,
                                                                                   self.bot.user.discriminator))
                try:
                    yield from self.bot.move_member(bot, self.vchannel)
                    try:
                        message_data = str(self.bot.botmessages['move_command_data'][0]).format(self.vchannel.name)
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                except discord.errors.InvalidArgument:
                    try:
                        message_data = str(self.bot.botmessages['move_command_data'][1])
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                except discord.errors.Forbidden:
                    try:
                        msgdata = str(self.bot.botmessages['move_command_data'][2]).format(self.vchannel.name)
                        message_data = msgdata
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                    except discord.errors.HTTPException:
                        try:
                            message_data = str(self.bot.botmessages['move_command_data'][3]).format(self.vchannel.name)
                            yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(self.bot, ctx)
            else:
                return

    @commands.command(name='LeaveVoiceChannel', pass_context=True, no_pm=True)
    @async
    def leave_voice_channel_command(self, ctx):
        """
        Bot Voice Command.
        :param ctx: Command Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        elif self.voice is not None:
            if self.voice_message_channel is not None:
                if ctx.message.channel.id == self.voice_message_channel.id:
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
                    filename = "{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json".format(self.bot.path,
                                                                                            self.bot.sepa)
                    json.dump(self.botvoicechannel, open(filename, "w"))
                    try:
                        try:
                            message_data = str(self.bot.botmessages['leave_voice_channel_command_data'][0]).format(
                                self.vchannel.name)
                        except AttributeError:
                            message_data = str(self.bot.botmessages['leave_voice_channel_command_data'][0]).format(
                                self.vchannel_name)
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
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
            msgdata = str(self.bot.botmessages['leave_voice_channel_command_data'][1])
            message_data = msgdata
            yield from self.bot.send_message(ctx.message.channel, message_data)

    @commands.command(name='Playlist', pass_context=True, no_pm=True)
    @async
    def playlist_command(self, ctx):
        """
        Bot Voice Command.
        :param ctx: Command Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        elif self.voice is not None:
            if self.voice_message_channel is not None:
                if ctx.message.channel.id == self.voice_message_channel.id:
                    track1 = str(self.bot.botmessages['playlist_command_data'][0])
                    track2 = str(self.bot.botmessages['playlist_command_data'][0])
                    track3 = str(self.bot.botmessages['playlist_command_data'][0])
                    track4 = str(self.bot.botmessages['playlist_command_data'][0])
                    track5 = str(self.bot.botmessages['playlist_command_data'][0])
                    track6 = str(self.bot.botmessages['playlist_command_data'][0])
                    track7 = str(self.bot.botmessages['playlist_command_data'][0])
                    track8 = str(self.bot.botmessages['playlist_command_data'][0])
                    track9 = str(self.bot.botmessages['playlist_command_data'][0])
                    track10 = str(self.bot.botmessages['playlist_command_data'][0])
                    if len(self.bot_playlist_entries) == 0:
                        track1 = str(self.bot.botmessages['playlist_command_data'][0])
                        track2 = str(self.bot.botmessages['playlist_command_data'][0])
                        track3 = str(self.bot.botmessages['playlist_command_data'][0])
                        track4 = str(self.bot.botmessages['playlist_command_data'][0])
                        track5 = str(self.bot.botmessages['playlist_command_data'][0])
                        track6 = str(self.bot.botmessages['playlist_command_data'][0])
                        track7 = str(self.bot.botmessages['playlist_command_data'][0])
                        track8 = str(self.bot.botmessages['playlist_command_data'][0])
                        track9 = str(self.bot.botmessages['playlist_command_data'][0])
                        track10 = str(self.bot.botmessages['playlist_command_data'][0])
                    elif len(self.bot_playlist_entries) == 1:
                        track1 = str(self.bot_playlist_entries[0])
                        track2 = str(self.bot.botmessages['playlist_command_data'][0])
                        track3 = str(self.bot.botmessages['playlist_command_data'][0])
                        track4 = str(self.bot.botmessages['playlist_command_data'][0])
                        track5 = str(self.bot.botmessages['playlist_command_data'][0])
                        track6 = str(self.bot.botmessages['playlist_command_data'][0])
                        track7 = str(self.bot.botmessages['playlist_command_data'][0])
                        track8 = str(self.bot.botmessages['playlist_command_data'][0])
                        track9 = str(self.bot.botmessages['playlist_command_data'][0])
                        track10 = str(self.bot.botmessages['playlist_command_data'][0])
                    elif len(self.bot_playlist_entries) == 2:
                        track1 = str(self.bot_playlist_entries[0])
                        track2 = str(self.bot_playlist_entries[1])
                        track3 = str(self.bot.botmessages['playlist_command_data'][0])
                        track4 = str(self.bot.botmessages['playlist_command_data'][0])
                        track5 = str(self.bot.botmessages['playlist_command_data'][0])
                        track6 = str(self.bot.botmessages['playlist_command_data'][0])
                        track7 = str(self.bot.botmessages['playlist_command_data'][0])
                        track8 = str(self.bot.botmessages['playlist_command_data'][0])
                        track9 = str(self.bot.botmessages['playlist_command_data'][0])
                        track10 = str(self.bot.botmessages['playlist_command_data'][0])
                    elif len(self.bot_playlist_entries) == 3:
                        track1 = str(self.bot_playlist_entries[0])
                        track2 = str(self.bot_playlist_entries[1])
                        track3 = str(self.bot_playlist_entries[2])
                        track4 = str(self.bot.botmessages['playlist_command_data'][0])
                        track5 = str(self.bot.botmessages['playlist_command_data'][0])
                        track6 = str(self.bot.botmessages['playlist_command_data'][0])
                        track7 = str(self.bot.botmessages['playlist_command_data'][0])
                        track8 = str(self.bot.botmessages['playlist_command_data'][0])
                        track9 = str(self.bot.botmessages['playlist_command_data'][0])
                        track10 = str(self.bot.botmessages['playlist_command_data'][0])
                    elif len(self.bot_playlist_entries) == 4:
                        track1 = str(self.bot_playlist_entries[0])
                        track2 = str(self.bot_playlist_entries[1])
                        track3 = str(self.bot_playlist_entries[2])
                        track4 = str(self.bot_playlist_entries[3])
                        track5 = str(self.bot.botmessages['playlist_command_data'][0])
                        track6 = str(self.bot.botmessages['playlist_command_data'][0])
                        track7 = str(self.bot.botmessages['playlist_command_data'][0])
                        track8 = str(self.bot.botmessages['playlist_command_data'][0])
                        track9 = str(self.bot.botmessages['playlist_command_data'][0])
                        track10 = str(self.bot.botmessages['playlist_command_data'][0])
                    elif len(self.bot_playlist_entries) == 5:
                        track1 = str(self.bot_playlist_entries[0])
                        track2 = str(self.bot_playlist_entries[1])
                        track3 = str(self.bot_playlist_entries[2])
                        track4 = str(self.bot_playlist_entries[3])
                        track5 = str(self.bot_playlist_entries[4])
                        track6 = str(self.bot.botmessages['playlist_command_data'][0])
                        track7 = str(self.bot.botmessages['playlist_command_data'][0])
                        track8 = str(self.bot.botmessages['playlist_command_data'][0])
                        track9 = str(self.bot.botmessages['playlist_command_data'][0])
                        track10 = str(self.bot.botmessages['playlist_command_data'][0])
                    elif len(self.bot_playlist_entries) == 6:
                        track1 = str(self.bot_playlist_entries[0])
                        track2 = str(self.bot_playlist_entries[1])
                        track3 = str(self.bot_playlist_entries[2])
                        track4 = str(self.bot_playlist_entries[3])
                        track5 = str(self.bot_playlist_entries[4])
                        track6 = str(self.bot_playlist_entries[5])
                        track7 = str(self.bot.botmessages['playlist_command_data'][0])
                        track8 = str(self.bot.botmessages['playlist_command_data'][0])
                        track9 = str(self.bot.botmessages['playlist_command_data'][0])
                        track10 = str(self.bot.botmessages['playlist_command_data'][0])
                    elif len(self.bot_playlist_entries) == 7:
                        track1 = str(self.bot_playlist_entries[0])
                        track2 = str(self.bot_playlist_entries[1])
                        track3 = str(self.bot_playlist_entries[2])
                        track4 = str(self.bot_playlist_entries[3])
                        track5 = str(self.bot_playlist_entries[4])
                        track6 = str(self.bot_playlist_entries[5])
                        track7 = str(self.bot_playlist_entries[6])
                        track8 = str(self.bot.botmessages['playlist_command_data'][0])
                        track9 = str(self.bot.botmessages['playlist_command_data'][0])
                        track10 = str(self.bot.botmessages['playlist_command_data'][0])
                    elif len(self.bot_playlist_entries) == 8:
                        track1 = str(self.bot_playlist_entries[0])
                        track2 = str(self.bot_playlist_entries[1])
                        track3 = str(self.bot_playlist_entries[2])
                        track4 = str(self.bot_playlist_entries[3])
                        track5 = str(self.bot_playlist_entries[4])
                        track6 = str(self.bot_playlist_entries[5])
                        track7 = str(self.bot_playlist_entries[6])
                        track8 = str(self.bot_playlist_entries[7])
                        track9 = str(self.bot.botmessages['playlist_command_data'][0])
                        track10 = str(self.bot.botmessages['playlist_command_data'][0])
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
                        track10 = str(self.bot.botmessages['playlist_command_data'][0])
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
                    msgdata = str(self.bot.botmessages['playlist_command_data'][1]).format(track1, track2, track3,
                                                                                           track4, track5, track6,
                                                                                           track7, track8, track9,
                                                                                           track10)
                    message_data = msgdata
                    yield from self.bot.send_message(ctx.message.channel, content=message_data)

    @commands.command(name='vol', pass_context=True, no_pm=True)
    @async
    def vol_command(self, ctx):
        """
        Bot Voice Command.
        :param ctx: Command Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        elif self.voice_message_channel is not None:
            if ctx.message.channel.id == self.voice_message_channel.id:
                if self.player is not None:
                    value_string = ctx.message.content.strip(self.bot.bot_prefix + "vol ")
                    try:
                        value = int(value_string) / 100
                        if 0.0 <= value <= 2.0:
                            self.player.volume = value
                            value_message = str(self.bot.botmessages['volume_command_data'][0]).format(str(value * 100))
                            yield from self.bot.send_message(self.voice_message_channel, content=value_message)
                        else:
                            yield from self.bot.send_message(self.voice_message_channel,
                                                             content=str(
                                                                 self.bot.botmessages['volume_command_data'][1]))
                    except ValueError:
                        yield from self.bot.send_message(self.voice_message_channel,
                                                         content=str(self.bot.botmessages['volume_command_data'][2]))
            else:
                yield from self.bot.send_message(self.voice_message_channel,
                                                 content=str(self.bot.botmessages['volume_command_data'][3]))

    # The function below needs to be able to be sent after the player completes to actually iterate
    # through the playlist.
    # NOTE: When an Exception happens in this after I have to pass the exception to silent it.

    def voice_playlist(self):
        """
        Listens for when music stops playing.
        :return: Nothing.
        """
        discord.compat.run_coroutine_threadsafe(self.playlist_iterator(), loop=self.bot.loop)

    @async
    def playlist_iterator(self):
        """
        Bot's Playlist Iterator.
        :return: Nothing.
        """
        if self.player.error is None:
            if self.voice_message_channel is not None:
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
                        message_data = str(self.bot.botmessages['auto_playlist_data'][0]).format(
                            str(self.player.title), str(self.player.uploader), minutes, seconds)
                        yield from self.bot.send_message(self.voice_message_channel, content=message_data)
                    except discord.errors.Forbidden:
                        pass
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
                                data, ytdl_options=self.ytdlo, options=self.ffmop, after=self.voice_playlist)
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
                                    track_info = str(self.bot.botmessages['auto_playlist_data'][1]).format(
                                        str(self.player.title),
                                        str(self.player.uploader))
                                    message_data = str(self.bot.botmessages['auto_playlist_data'][2]).format(
                                        track_info, minutes, seconds)
                                    yield from self.bot.send_message(self.voice_message_channel,
                                                                     content=message_data)
                                    try:
                                        self.bot_playlist_entries.remove(track_info)
                                    except ValueError:
                                        pass
                                except discord.errors.Forbidden:
                                    pass
                                if self.player is not None:
                                    self.player.start()
                    except UnboundLocalError:
                        self.is_bot_playing = False
        else:
            if self.voice_message_channel is not None:
                yield from self.bot.send_message(self.voice_message_channel,
                                                 content="A Error Occured while playing. {0}".format(
                                                     self.player.error))


def setup(bot):
    """
    Voice Commands.
    """
    cog = VoiceBotCommands(bot)
    cog.setup()
    bot.add_cog(cog)
