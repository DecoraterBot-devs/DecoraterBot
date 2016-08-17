# coding=utf-8
"""
    DecoraterBot's source is protected by Cheese.lab industries Inc. Even though it is Open Source
    any and all users waive the right to say that this bot's code was stolen when it really was not.
    Me @Decorater the only core developer of this bot do not take kindly to those false Allegations.
    it would piss any DEVELOPER OFF WHEN THEY SPEND ABOUT A YEAR CODING STUFF FROM SCRATCH AND THEN BE ACCUSED OF
    SHIT LIKE THIS.
    
    So, do not do it. If you do Cheese.lab Industries Inc. Can and Will do after you for such cliams that it deems
    untrue.
    
    Cheese.lab industries Inc. Belieces in the rights of Original Developers of bots. They do not take kindly to
    BULLSHIT.
    
    Any and all Developers work all the time, many of them do not get paid for their hard work.
    
    I am one of those who did not get paid even though I am the original Developer I coded this bot from the bottom
    with no lines of code at all.
    
    And how much money did I get from it for my 11 months or so of working on it? None, yeah thats right 0$ how
    pissed can someone get?
    Exactly I have over stretched my relatives money that they paid for Internet and power for my computer so that
    way I can code my bot.
    
    However shit does go out of the Fan with a possible 600$ or more that my Laptop Drastically needs to Repairs as
    it is 10 years old and is falling apart
    
    I am half tempted myself to pulling this bot from github and making it on patrion that boobot was on to help me
    with my development needs.
    
    So, as such I accept issue requests, but please do not give me bullshit I hate it as it makes everything worse
    than the way it is.
    
    You do have the right however to:
        --> Contribute to the bot's development.
        --> fix bugs.
        --> add commands.
        --> help finish the per server config (has issues)
        --> update the Voice commands to be better (and not use globals which is 1 big thing that kills it).
        --> Use the code for your own bot. Put Please give me the Credits for at least mot of the code. And Yes you can
                bug fix all you like.
                But Please try to share your bug fixes with me (if stable) I would gladly Accept bug fixes that fixes
                any and/or all issues.
                (There are times when I am so busy that I do not see or even notice some bugs for a few weeks or more)

    But keep in mind any and all Changes you make can and will be property of Cheese.lab Industries Inc.
"""
from __future__ import unicode_literals
import discord
import asyncio
import json
import io
import traceback
import urllib
import sys
import os
import base64
import os.path
import random
import concurrent
import platform
import youtube_dl
import time
import cmath
import ctypes
import subprocess
from threading import Timer
from collections import deque
import BotPMError
from discord.ext import commands

sepa = os.sep

botbanslist = io.open('{0}{1}resources{1}ConfigData{1}BotBanned.json'.format(sys.path[0], sepa), 'r')
banlist = json.load(botbanslist)
botbanslist.close()
try:
    botvoicechannelfile = io.open('{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json'.format(sys.path[0], sepa), 'r')
    botvoicechannel = json.load(botvoicechannelfile)
    botvoicechannelfile.close()
except FileNotFoundError:
    pass
botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.json'.format(sys.path[0], sepa), 'r')
botmessages = json.load(botmessagesdata)
botmessagesdata.close()

PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(sys.path[0], sepa)
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    credsfile = io.open(PATH, 'r')
    credentials = json.load(credsfile)
    credsfile.close()
    _bot_prefix = str(credentials['bot_prefix'][0])
    _log_ytdl = str(credentials['ytdl_logs'][0])
    if _log_ytdl == 'True':
        _log_ytdl = True
    elif _log_ytdl == 'False':
        _log_ytdl = False

bits = ctypes.sizeof(ctypes.c_voidp)
# I Sadly have only Windows Version of opus.dll ad Windows Version of FFmpeg.
# Feel free to help pull request Linux & Mac versions of these files especially the pyd's.
# Hopefully they will not conflict with the windows pyd's
# Why? Because I don't have a Mac or a Linux OS.
if bits == 4:
    opusdll = "{0}{1}resources{1}opus{1}opus.dll".format(sys.path[0], sepa)
    os.chdir("{0}{1}resources{1}ffmpeg{1}x86".format(sys.path[0], sepa))
elif bits == 8:
    opusdll = "{0}{1}resources{1}opus{1}opus64.dll".format(sys.path[0], sepa)
    os.chdir("{0}{1}resources{1}ffmpeg{1}x64".format(sys.path[0], sepa))


class YTDLLogger(object):
    def log_file_code(self, meth, msg):
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
        if _log_ytdl:
            self.log_file_code('ytdl_info', msg)
        else:
            pass

    def debug(self, msg):
        if _log_ytdl:
            self.log_file_code('ytdl_debug', msg)
        else:
            pass

    def warning(self, msg):
        if _log_ytdl:
            self.log_file_code('ytdl_warning', msg)
        else:
            pass

    def error(self, msg):
        if _log_ytdl:
            self.log_file_code('ytdl_error', msg)
        else:
            pass


# noinspection PyGlobalUndefined
global ytdlo
# noinspection PyGlobalUndefined
global player
# noinspection PyGlobalUndefined
global vchannel
# noinspection PyGlobalUndefined
global vchannel_name
# noinspection PyGlobalUndefined
global voice_message_channel
# noinspection PyGlobalUndefined
global voice_message_server
# noinspection PyGlobalUndefined
global voice_message_server_name
# noinspection PyGlobalUndefined
global voice
# noinspection PyGlobalUndefined
global _sent_finished_message
# noinspection PyGlobalUndefined
global sent_prune_error_message
# noinspection PyGlobalUndefined
global is_bot_playing
# noinspection PyGlobalUndefined
global bot_playlist
# noinspection PyGlobalUndefined
global bot_playlist_entries
# noinspection PyGlobalUndefined
global _temp_player_1
# noinspection PyGlobalUndefined
global _temp_player_2
# noinspection PyGlobalUndefined
global _temp_player_3
# noinspection PyGlobalUndefined
global _temp_player_4
# noinspection PyGlobalUndefined
global _temp_player_5
# noinspection PyGlobalUndefined
global _temp_player_6
# noinspection PyGlobalUndefined
global _temp_player_7
# noinspection PyGlobalUndefined
global _temp_player_8
# noinspection PyGlobalUndefined
global _temp_player_9
# noinspection PyGlobalUndefined
global _temp_player_10
# noinspection PyGlobalUndefined
global ffmop
# noinspection PyGlobalUndefined
global ffmout
# noinspection PyGlobalUndefined
global verror

# noinspection PyRedeclaration
ytdlo = {'verbose': False, 'logger': YTDLLogger(), 'default_search': "ytsearch"}
# noinspection PyRedeclaration
player = None
# noinspection PyRedeclaration
vchannel = None
# noinspection PyRedeclaration
vchannel_name = None
# noinspection PyRedeclaration
voice_message_channel = None
# noinspection PyRedeclaration
voice_message_server = None
# noinspection PyRedeclaration
voice_message_server_name = None
# noinspection PyRedeclaration
voice = None
# noinspection PyRedeclaration
_sent_finished_message = False
# noinspection PyRedeclaration
sent_prune_error_message = False
# noinspection PyRedeclaration
is_bot_playing = False
# noinspection PyRedeclaration
bot_playlist = []
# noinspection PyRedeclaration
bot_playlist_entries = []
# noinspection PyRedeclaration
_temp_player_1 = None
# noinspection PyRedeclaration
_temp_player_2 = None
# noinspection PyRedeclaration
_temp_player_3 = None
# noinspection PyRedeclaration
_temp_player_4 = None
# noinspection PyRedeclaration
_temp_player_5 = None
# noinspection PyRedeclaration
_temp_player_6 = None
# noinspection PyRedeclaration
_temp_player_7 = None
# noinspection PyRedeclaration
_temp_player_8 = None
# noinspection PyRedeclaration
_temp_player_9 = None
# noinspection PyRedeclaration
_temp_player_10 = None
# noinspection PyRedeclaration
ffmop = "-nostats -loglevel quiet"
# noinspection PyRedeclaration
ffmout = io.open('{0}{1}resources{1}Logs{1}ffmpeg.shit'.format(sys.path[0], sepa), 'w')
# noinspection PyRedeclaration
verror = False


# noinspection PyExceptClausesOrder,PyPep8Naming,PyUnboundLocalVariable
class bot_data:
    """
        This class is for Internal use only!!!
    """
    def __init__(self):
        pass

    @asyncio.coroutine
    def voice_stuff_new_code(self, client, message):
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
                    yield from BotPMError._resolve_send_message_error(client, message)
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
                            msgdata = 'This Bot needs the PyNaCl library in order to use the voice commands. Please tell the Developer of this bot to Add it in.'
                            yield from client.send_message(voice_message_channel, msgdata)
                        if not verror:
                            try:
                                msg_data = str(botmessages['join_voice_channel_command_data'][1]).format(vchannel.name)
                                yield from client.send_message(message.channel, msg_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError._resolve_send_message_error(client, message)
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
                            yield from BotPMError._resolve_send_message_error(client, message)
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
                            yield from BotPMError._resolve_send_message_error(client, message)
                    except discord.errors.ClientException:
                        voice_message_channel = None
                        voice = None
                        vchannel = None
                        voice_message_server = None
                        try:
                            msg_data = str(botmessages['join_voice_channel_command_data'][4])
                            yield from client.send_message(message.channel, msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
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
                            yield from BotPMError._resolve_send_message_error(client, message)
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
                                        message_data = "You must Specify a URL in this command."
                                        yield from client.send_message(voice_message_channel, message_data)
                                    except discord.errors.Forbidden:
                                        yield from BotPMError._resolve_send_message_error(client, message)
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
                                                data = "] ["
                                                msgdata = str(player.title) + "] by [" + str(player.uploader) + data
                                                part1 = "**Now Playing ["
                                                message_data = part1 + msgdata + minutes + ":" + seconds + "]**"
                                                yield from client.send_message(voice_message_channel, message_data)
                                            except discord.errors.Forbidden:
                                                yield from BotPMError._resolve_send_message_error(client, message)
                                            try:
                                                player.start()
                                            except RuntimeError:
                                                pass
                                        except AttributeError:
                                            msgdata = 'Sorry, This Video must have either been deleted by the '
                                            part1 = msgdata + 'owner. And/or  their account was supspended/'
                                            messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                            message_data = messagedata + 'is not available in the United States.'
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
                                                    data = "] ["
                                                    msgdata = str(player.title) + "] by [" + str(player.uploader) + data
                                                    part1 = "**Now Playing ["
                                                    message_data = part1 + msgdata + minutes + ":" + seconds + "]**"
                                                    yield from client.send_message(voice_message_channel,
                                                                                   message_data)
                                                except discord.errors.Forbidden:
                                                    yield from BotPMError._resolve_send_message_error(client,
                                                                                                      message)
                                                try:
                                                    player.start()
                                                except RuntimeError:
                                                    pass
                                            except AttributeError:
                                                msgdata = 'Sorry, This Video must have either been deleted by the '
                                                part1 = msgdata + 'owner. And/or  their account was supspended/'
                                                messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                                message_data = messagedata + 'is not available in the United States.'
                                                is_bot_playing = False
                                                yield from client.send_message(voice_message_channel, message_data)
                                    else:
                                        message_data = 'The URL specified is nto a valid Youtube Video/Music URL.'
                                        yield from client.send_message(voice_message_channel, message_data)
                                        _temp_player_1 = None
                            except IndexError:
                                return
                            except urllib.error.URLError:
                                return
                            except discord.errors.ClientException:
                                msgdata = "Error: ffmpeg not found.\nCurrent Path Vars(With appeneds last 2 on end):"
                                message_data = msgdata + "```py\n" + str(sys.path) + "\n```"
                                yield from client.send_message(message.channel, message_data)
                                player = None
                            except youtube_dl.utils.ExtractorError:
                                message_data = "Error When trying to extract the video from the Youtube video URL."
                                yield from client.send_message(message.channel, message_data)
                                player = None
                            except youtube_dl.utils.UnsupportedError:
                                yield from client.send_message(message.channel, "Unsupported Youtube video URL.")
                                player = None
                            except youtube_dl.utils.DownloadError:
                                yield from client.send_message(message.channel, "Invalid or not a Youtube video URL.")
                                player = None
                        else:
                            return
                else:
                    message_data = "This bot needs to be in a voice channel to be able to use this command."
                    yield from client.send_message(message.channel, message_data)
            else:
                if player is not None:
                    data = message.content[len(_bot_prefix + "play "):].strip()
                    if data == "":
                        try:
                            message_data = "You must Specify a URL or a search term of a video in this command."
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
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
                                    track1 = '[' + playlist01 + ']'
                                    fulldir = playlist01time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = '[' + minutes + ':' + seconds + ']'
                                    track1time = newdir
                                    track1uploader = str(_temp_player_1.uploader)
                                    track1info = track1 + ' by [' + track1uploader + '] ' + track1time
                                    bot_playlist_entries.append(track1info)
                                    msgdata = '**' + track1 + track1time + '** has been added to my playlist.'
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    _temp_player_1.start()
                                    _temp_player_1.stop()
                                except AttributeError:
                                    msgdata = 'Sorry, This Video must have either been deleted by the owner. '
                                    part1 = msgdata + 'And/or  their account was supspended/'
                                    messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                    message_data = messagedata + 'is not available in the United States.'
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif data in bot_playlist:
                                msgdata = 'Sorry, that url is already in my playlist.'
                                message_data = msgdata
                                yield from client.send_message(message.channel, message_data)
                            elif len(bot_playlist) == 1:
                                _temp_player_2 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist02 = _temp_player_2.title
                                    playlist02time = _temp_player_2.duration
                                    track2 = '[' + playlist02 + ']'
                                    fulldir = playlist02time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = '[' + minutes + ':' + seconds + ']'
                                    track2time = newdir
                                    track2uploader = str(_temp_player_2.uploader)
                                    track2info = track2 + ' by [' + track2uploader + '] ' + track2time
                                    bot_playlist_entries.append(track2info)
                                    msgdata = '**' + track2 + track2time + '** has been added to my playlist.'
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    _temp_player_2.start()
                                    _temp_player_2.stop()
                                except AttributeError:
                                    msgdata = 'Sorry, This Video must have either been deleted by the owner. '
                                    part1 = msgdata + 'And/or  their account was supspended/'
                                    messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                    message_data = messagedata + 'is not available in the United States.'
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 2:
                                _temp_player_3 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist03 = _temp_player_3.title
                                    playlist03time = _temp_player_3.duration
                                    track3 = '[' + playlist03 + ']'
                                    fulldir = playlist03time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = '[' + minutes + ':' + seconds + ']'
                                    track3time = newdir
                                    track3uploader = str(_temp_player_3.uploader)
                                    track3info = track3 + ' by [' + track3uploader + '] ' + track3time
                                    bot_playlist_entries.append(track3info)
                                    msgdata = '**' + track3 + track3time + '** has been added to my playlist.'
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    _temp_player_3.start()
                                    _temp_player_3.stop()
                                except AttributeError:
                                    msgdata = 'Sorry, This Video must have either been deleted by the owner. '
                                    part1 = msgdata + 'And/or  their account was supspended/'
                                    messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                    message_data = messagedata + 'is not available in the United States.'
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 3:
                                _temp_player_4 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist04 = _temp_player_4.title
                                    playlist04time = _temp_player_4.duration
                                    track4 = '[' + playlist04 + ']'
                                    fulldir = playlist04time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = '[' + minutes + ':' + seconds + ']'
                                    track4time = newdir
                                    track4uploader = str(_temp_player_4.uploader)
                                    track4info = track4 + ' by [' + track4uploader + '] ' + track4time
                                    bot_playlist_entries.append(track4info)
                                    msgdata = '**' + track4 + track4time + '** has been added to my playlist.'
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    _temp_player_4.start()
                                    _temp_player_4.stop()
                                except AttributeError:
                                    msgdata = 'Sorry, This Video must have either been deleted by the owner. '
                                    part1 = msgdata + 'And/or  their account was supspended/'
                                    messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                    message_data = messagedata + 'is not available in the United States.'
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 4:
                                _temp_player_5 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist05 = _temp_player_5.title
                                    playlist05time = _temp_player_5.duration
                                    track5 = '[' + playlist05 + ']'
                                    fulldir = playlist05time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = '[' + minutes + ':' + seconds + ']'
                                    track5time = newdir
                                    track5uploader = str(_temp_player_5.uploader)
                                    track5info = track5 + ' by [' + track5uploader + '] ' + track5time
                                    bot_playlist_entries.append(track5info)
                                    msgdata = '**' + track5 + track5time + '** has been added to my playlist.'
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    _temp_player_5.start()
                                    _temp_player_5.stop()
                                except AttributeError:
                                    msgdata = 'Sorry, This Video must have either been deleted by the owner. '
                                    part1 = msgdata + 'And/or  their account was supspended/'
                                    messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                    message_data = messagedata + 'is not available in the United States.'
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 5:
                                _temp_player_6 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist06 = _temp_player_6.title
                                    playlist06time = _temp_player_6.duration
                                    track6 = '[' + playlist06 + ']'
                                    fulldir = playlist06time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = '[' + minutes + ':' + seconds + ']'
                                    track6time = newdir
                                    track6uploader = str(_temp_player_6.uploader)
                                    track6info = track6 + ' by [' + track6uploader + '] ' + track6time
                                    bot_playlist_entries.append(track6info)
                                    msgdata = '**' + track6 + track6time + '** has been added to my playlist.'
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    _temp_player_6.start()
                                    _temp_player_6.stop()
                                except AttributeError:
                                    msgdata = 'Sorry, This Video must have either been deleted by the owner. '
                                    part1 = msgdata + 'And/or  their account was supspended/'
                                    messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                    message_data = messagedata + 'is not available in the United States.'
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 6:
                                _temp_player_7 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist07 = _temp_player_7.title
                                    playlist07time = _temp_player_7.duration
                                    track7 = '[' + playlist07 + ']'
                                    fulldir = playlist07time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = '[' + minutes + ':' + seconds + ']'
                                    track7time = newdir
                                    track7uploader = str(_temp_player_7.uploader)
                                    track7info = track7 + ' by [' + track7uploader + '] ' + track7time
                                    bot_playlist_entries.append(track7info)
                                    msgdata = '**' + track7 + track7time + '** has been added to my playlist.'
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    _temp_player_7.start()
                                    _temp_player_7.stop()
                                except AttributeError:
                                    msgdata = 'Sorry, This Video must have either been deleted by the owner. '
                                    part1 = msgdata + 'And/or  their account was supspended/'
                                    messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                    message_data = messagedata + 'is not available in the United States.'
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 7:
                                _temp_player_8 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist08 = _temp_player_8.title
                                    playlist08time = _temp_player_8.duration
                                    track8 = '[' + playlist08 + ']'
                                    fulldir = playlist08time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = '[' + minutes + ':' + seconds + ']'
                                    track8time = newdir
                                    track8uploader = str(_temp_player_8.uploader)
                                    track8info = track8 + ' by [' + track8uploader + '] ' + track8time
                                    bot_playlist_entries.append(track8info)
                                    msgdata = '**' + track8 + track8time + '** has been added to my playlist.'
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    _temp_player_8.start()
                                    _temp_player_8.stop()
                                except AttributeError:
                                    msgdata = 'Sorry, This Video must have either been deleted by the owner. '
                                    part1 = msgdata + 'And/or  their account was supspended/'
                                    messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                    message_data = messagedata + 'is not available in the United States.'
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 8:
                                _temp_player_9 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                     options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist09 = _temp_player_9.title
                                    playlist09time = _temp_player_9.duration
                                    track9 = '[' + playlist09 + ']'
                                    fulldir = playlist09time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = '[' + minutes + ':' + seconds + ']'
                                    track9time = newdir
                                    track9uploader = str(_temp_player_9.uploader)
                                    track9info = track9 + ' by [' + track9uploader + '] ' + track9time
                                    bot_playlist_entries.append(track9info)
                                    msgdata = '**' + track9 + track9time + '** has been added to my playlist.'
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    _temp_player_9.start()
                                    _temp_player_9.stop()
                                except AttributeError:
                                    msgdata = 'Sorry, This Video must have either been deleted by the owner. '
                                    part1 = msgdata + 'And/or  their account was supspended/'
                                    messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                    message_data = messagedata + 'is not available in the United States.'
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 9:
                                _temp_player_10 = yield from voice.create_ytdl_player(data, ytdl_options=ytdlo,
                                                                                      options=ffmop, output=ffmout)
                                bot_playlist.append(data)
                                try:
                                    playlist10 = _temp_player_10.title
                                    playlist10time = _temp_player_10.duration
                                    track10 = '[' + playlist10 + ']'
                                    fulldir = playlist10time
                                    minutes = str(int((fulldir / 60) % 60))
                                    seconds = str(int(fulldir % 60))
                                    if len(seconds) == 1:
                                        seconds = "0" + seconds
                                    newdir = '[' + minutes + ':' + seconds + ']'
                                    track10time = newdir
                                    track10uploader = str(_temp_player_10.uploader)
                                    track10info = track10 + ' by [' + track10uploader + '] ' + track10time
                                    bot_playlist_entries.append(track10info)
                                    msgdata = '**' + track10 + track10time + '** has been added to my playlist.'
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                    _temp_player_10.start()
                                    _temp_player_10.stop()
                                except AttributeError:
                                    msgdata = 'Sorry, This Video must have either been deleted by the owner. '
                                    part1 = msgdata + 'And/or  their account was supspended/'
                                    messagedata = part1 + 'terminated by Youtube. **Or** the video '
                                    message_data = messagedata + 'is not available in the United States.'
                                    yield from client.send_message(voice_message_channel, message_data)
                            elif len(bot_playlist) == 10:
                                msgdata = 'Sorry, my playlist is full right now.'
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
                            msgdata = str(player.title) + "] by [" + str(player.uploader) + "] ["
                            message_data = "**Stopped [" + msgdata + minutes + ":" + seconds + "]**"
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
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
                                            track_info = str(player.title) + "] by [" + str(player.uploader) + "] ["
                                            track_info2 = track_info + minutes + ":" + seconds + "]"
                                            message_data = "**Now Playing [" + track_info2 + "**"
                                            yield from client.send_message(voice_message_channel, message_data)
                                            try:
                                                bot_playlist_entries.remove(track_info)
                                            except ValueError:
                                                pass
                                        except discord.errors.Forbidden:
                                            yield from BotPMError._resolve_send_message_error(client, message)
                                        player.start()
                            except UnboundLocalError:
                                player = None
                                is_bot_playing = False
                    else:
                        try:
                            message_data = "Failed to stop the currently playing song/whatever it is as player is None."
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
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
                            msgdata = str(player.title) + "] by [" + str(player.uploader) + "] ["
                            message_data = "**Paused [" + msgdata + minutes + ":" + seconds + "]**"
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
                        player.pause()
                    else:
                        message_data = "Failed to pause the currently playing song/whatever it is as player is None."
                        yield from client.send_message(voice_message_channel, message_data)
                else:
                    return
            else:
                message_data = 'This bot must be in a voice channel to be able to pause a Youtube Video/Music.'
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
                            msgdata = str(player.title) + "] by [" + str(player.uploader) + "] ["
                            message_data = "**Resumed [" + msgdata + minutes + ":" + seconds + "]**"
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
                        player.resume()
                    else:
                        try:
                            msgdata = "Failed to resume the currently playing song/whatever it is as player is None."
                            message_data = msgdata
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
                else:
                    return
            else:
                message_data = 'This bot must be in a voice channel to be able to unpause a Youtube Video/Music.'
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
                            message_data = 'Moved to the ' + vchannel.name + " Voice Channel."
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
                    except discord.errors.InvalidArgument:
                        try:
                            message_data = 'The Channel specified is not a voice channel.'
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
                    except discord.errors.Forbidden:
                        try:
                            msgdata = 'This bot does not have permissions to move members to the '
                            message_data = msgdata + vchannel.name + ' Voice Channel.'
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
                        except discord.errors.HTTPException:
                            try:
                                message_data = 'Failed to move to the ' + vchannel.name + ' Voice Channel.'
                                yield from client.send_message(voice_message_channel, message_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError._resolve_send_message_error(client, message)
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
                            track_info = str(player.title) + "] by [" + str(player.uploader) + "] [" + minutes + ":"
                            message_data = "**Finished [" + track_info + seconds + "]**"
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
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
                                        track_info = str(player.title) + "] by [" + str(player.uploader) + "] ["
                                        track_info2 = track_info + minutes + ":" + seconds + "]"
                                        message_data = "**Now Playing [" + track_info2 + "**"
                                        yield from client.send_message(voice_message_channel, message_data)
                                        try:
                                            bot_playlist_entries.remove(track_info)
                                        except ValueError:
                                            pass
                                    except discord.errors.Forbidden:
                                        yield from BotPMError._resolve_send_message_error(client, message)
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
                                message_data = "Left the " + vchannel.name + " Voice Channel."
                            except AttributeError:
                                message_data = "Left the " + vchannel_name + " Voice Channel."
                            yield from client.send_message(voice_message_channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
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
                msgdata = 'This bot does not have a Voice Channel to leave.'
                message_data = msgdata
                yield from client.send_message(message.channel, message_data)
        if message.content.startswith(_bot_prefix + 'Playlist'):
            track1 = 'Empty[00:00]'
            track2 = 'Empty[00:00]'
            track3 = 'Empty[00:00]'
            track4 = 'Empty[00:00]'
            track5 = 'Empty[00:00]'
            track6 = 'Empty[00:00]'
            track7 = 'Empty[00:00]'
            track8 = 'Empty[00:00]'
            track9 = 'Empty[00:00]'
            track10 = 'Empty[00:00]'
            if message.author.id in banlist['Users']:
                return
            elif len(bot_playlist_entries) == 0:
                track1 = 'Empty[00:00]'
                track2 = 'Empty[00:00]'
                track3 = 'Empty[00:00]'
                track4 = 'Empty[00:00]'
                track5 = 'Empty[00:00]'
                track6 = 'Empty[00:00]'
                track7 = 'Empty[00:00]'
                track8 = 'Empty[00:00]'
                track9 = 'Empty[00:00]'
                track10 = 'Empty[00:00]'
            elif len(bot_playlist_entries) == 1:
                track1 = str(bot_playlist_entries[0])
                track2 = 'Empty[00:00]'
                track3 = 'Empty[00:00]'
                track4 = 'Empty[00:00]'
                track5 = 'Empty[00:00]'
                track6 = 'Empty[00:00]'
                track7 = 'Empty[00:00]'
                track8 = 'Empty[00:00]'
                track9 = 'Empty[00:00]'
                track10 = 'Empty[00:00]'
            elif len(bot_playlist_entries) == 2:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = 'Empty[00:00]'
                track4 = 'Empty[00:00]'
                track5 = 'Empty[00:00]'
                track6 = 'Empty[00:00]'
                track7 = 'Empty[00:00]'
                track8 = 'Empty[00:00]'
                track9 = 'Empty[00:00]'
                track10 = 'Empty[00:00]'
            elif len(bot_playlist_entries) == 3:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = 'Empty[00:00]'
                track5 = 'Empty[00:00]'
                track6 = 'Empty[00:00]'
                track7 = 'Empty[00:00]'
                track8 = 'Empty[00:00]'
                track9 = 'Empty[00:00]'
                track10 = 'Empty[00:00]'
            elif len(bot_playlist_entries) == 4:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = 'Empty[00:00]'
                track6 = 'Empty[00:00]'
                track7 = 'Empty[00:00]'
                track8 = 'Empty[00:00]'
                track9 = 'Empty[00:00]'
                track10 = 'Empty[00:00]'
            elif len(bot_playlist_entries) == 5:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(bot_playlist_entries[4])
                track6 = 'Empty[00:00]'
                track7 = 'Empty[00:00]'
                track8 = 'Empty[00:00]'
                track9 = 'Empty[00:00]'
                track10 = 'Empty[00:00]'
            elif len(bot_playlist_entries) == 6:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(bot_playlist_entries[4])
                track6 = str(bot_playlist_entries[5])
                track7 = 'Empty[00:00]'
                track8 = 'Empty[00:00]'
                track9 = 'Empty[00:00]'
                track10 = 'Empty[00:00]'
            elif len(bot_playlist_entries) == 7:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(bot_playlist_entries[4])
                track6 = str(bot_playlist_entries[5])
                track7 = str(bot_playlist_entries[6])
                track8 = 'Empty[00:00]'
                track9 = 'Empty[00:00]'
                track10 = 'Empty[00:00]'
            elif len(bot_playlist_entries) == 8:
                track1 = str(bot_playlist_entries[0])
                track2 = str(bot_playlist_entries[1])
                track3 = str(bot_playlist_entries[2])
                track4 = str(bot_playlist_entries[3])
                track5 = str(bot_playlist_entries[4])
                track6 = str(bot_playlist_entries[5])
                track7 = str(bot_playlist_entries[6])
                track8 = str(bot_playlist_entries[7])
                track9 = 'Empty[00:00]'
                track10 = 'Empty[00:00]'
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
                track10 = 'Empty[00:00]'
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
            msgdata = "Track 0 : **{0}**\nTrack 1 : **{1}**\nTrack 2 : **{2}**\nTrack 3 : **{3}**\nTrack 4 : **{4}**\nTrack 5 : **{5}**\nTrack 6 : **{6}**\nTrack 7 : **{7}**\nTrack 8 : **{8}**\nTrack 9 : **{9}**".format(track1, track2, track3, track4, track5, track6, track7, track8, track9, track10)
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
                                value_message = "Volume changed to ``{0}%``".format(value_string)
                                yield from client.send_message(voice_message_channel, value_message)
                            else:
                                yield from client.send_message(voice_message_channel, "Sorry, volume can only be within the range of 0~200. Please try again.")
                        except ValueError:
                            yield from client.send_message(voice_message_channel, "Sorry, you must specify a actual int value to change the volume.")
                else:
                    yield from client.send_message(voice_message_channel, "Sorry, you can only use this when the bot is playing something.")

    @asyncio.coroutine
    def voice_stuff_new_disabled_code(self, client, message):
        """
            :rtype: Message object
            :param client: Discord.py Client Object
            :param message: Message Object
        """
        if message.content.startswith(_bot_prefix + 'JoinVoiceChannel'):
            msgdata = "Sorry, Voice Commands are Disabled."
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'play'):
            msgdata = "Sorry, Voice Commands are Disabled."
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'stop'):
            msgdata = "Sorry, Voice Commands are Disabled."
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'pause'):
            msgdata = "Sorry, Voice Commands are Disabled."
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'unpause'):
            msgdata = "Sorry, Voice Commands are Disabled."
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'move'):
            msgdata = "Sorry, Voice Commands are Disabled."
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'LeaveVoiceChannel'):
            msgdata = "Sorry, Voice Commands are Disabled."
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + 'Playlist'):
            msgdata = "Sorry, Voice Commands are Disabled."
            yield from client.send_message(message.channel, msgdata)
        if message.content.startswith(_bot_prefix + "vol"):
            msgdata = "Sorry, Voice Commands are Disabled."
            yield from client.send_message(message.channel, msgdata)

    @asyncio.coroutine
    def _reload_commands_bypass1_new_code(self, client, message, reload_reason):
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
                            message_data = "Left the {0} Voice Channel. Reason: {1}".format(vchannel.name,
                                                                                            reload_reason)
                        except AttributeError:
                            message_data = "Left the {0} Voice Channel. Reason: {1}".format(vchannel_name,
                                                                                            reload_reason)
                    else:
                        reason = 'Owner is reloading Voice Channel Commands.'
                        try:
                            message_data = "Left the {0} Voice Channel. Reason: {1}".format(vchannel.name, reason)
                        except AttributeError:
                            message_data = "Left the {0} Voice Channel. Reason: {1}".format(vchannel_name, reason)
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
                    yield from BotPMError._resolve_send_message_error(client, message)

    @asyncio.coroutine
    def _reload_commands_bypass2_new_code(self, client, message):
        global vchannel
        global voice
        global voice_message_server
        global voice_message_channel
        global voice_message_server_name
        global vchannel_name
        global verror
        try:
            botvoicechannelfile = io.open('{0}{1}resources{1}ConfigData{1}BotVoiceChannel.json'.format(sys.path[0], sepa), 'r')
            botvoicechannel_reloaded = json.load(botvoicechannelfile)
            botvoicechannelfile.close()
        except FileNotFoundError:
            pass
        try:
            # noinspection PyUnboundLocalVariable
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
                yield from client.send_message(message.channel, "A Timeout Error Kept the bot from Rejoining the Voice Channel.")
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
                msgdata = 'This Bot needs the PyNaCl library in order to use the voice commands. Please tell the Developer of this bot to Add it in.'
                yield from client.send_message(voice_message_channel, msgdata)
            if verror is not True:
                message_data = "Rejoined the {0} Voice Channel.".format(vchannel_name)
                yield from client.send_message(voice_message_channel, message_data)
        except IndexError:
            voice_message_server_name = None
            vchannel_name = None
            vchannel = None
            voice_message_server = None
            voice_message_channel = None
            voice = None

    @asyncio.coroutine
    def _reload_commands_bypass3_new_code(self, client):
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
                msgdata = 'This Bot needs the PyNaCl library in order to use the voice commands. Please tell the Developer of this bot to Add it in.'
                yield from client.send_message(voice_message_channel, msgdata)
            if verror is not True:
                message_data = "Rejoined the {0} Voice Channel.".format(vchannel_name)
                yield from client.send_message(voice_message_channel, message_data)
        except IndexError:
            voice_message_server_name = None
            vchannel_name = None
            vchannel = None
            voice_message_server = None
            voice_message_channel = None
            voice = None

    @asyncio.coroutine
    def _reload_commands_bypass4_new_code(self, client, message, reload_reason):
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
                            message_data = "Left the {0} Voice Channel. Reason: {1}".format(vchannel.name,
                                                                                            reload_reason)
                        except AttributeError:
                            message_data = "Left the {0} Voice Channel. Reason: {1}".format(vchannel_name,
                                                                                            reload_reason)
                    else:
                        reason = 'Owner is doing a high level reload.'
                        try:
                            message_data = "Left the {0} Voice Channel. Reason: {1}".format(vchannel.name, reason)
                        except AttributeError:
                            message_data = "Left the {0} Voice Channel. Reason: {1}".format(vchannel_name, reason)
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
                    yield from BotPMError._resolve_send_message_error(client, message)


class VoiceBotCommands:
    def __init__(self):
        self.bot = bot_data()

    @asyncio.coroutine
    def voice_stuff_new(self, client, message):
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
    def _reload_commands_bypass1_new(self, client, message, reload_reason):
        yield from self.bot._reload_commands_bypass1_new_code(client, message, reload_reason)

    @asyncio.coroutine
    def _reload_commands_bypass2_new(self, client, message):
        yield from self.bot._reload_commands_bypass2_new_code(client, message)

    @asyncio.coroutine
    def _reload_commands_bypass3_new(self, client):
        yield from self.bot._reload_commands_bypass3_new_code(client)

    @asyncio.coroutine
    def _reload_commands_bypass4_new(self, client, message, reload_reason):
        yield from self.bot._reload_commands_bypass4_new_code(client, message, reload_reason)
