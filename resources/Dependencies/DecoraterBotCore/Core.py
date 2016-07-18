# coding=utf-8
import os
import discord
import requests
import ctypes
import sys
import subprocess
import time
import asyncio
import json
import traceback
import importlib
import io
try:
    import Ignore
except ImportError:
    sys.path.append(sys.path[0] + "\\resources\\Dependencies\\DecoraterBotCore")
    import Ignore
import Login
import BotCommands
import BotPMError
import BotVoiceCommands
from discord.ext import commands

jsonfile = io.open(sys.path[0] + '\\resources\\ConfigData\\BotBanned.json', 'r')
somedict = json.load(jsonfile)
consoledatafile = io.open(sys.path[0] + '\\resources\ConfigData\\ConsoleWindow.json', 'r')
consoletext = json.load(consoledatafile)
botmessagesdata = io.open(sys.path[0] + '\\resources\\ConfigData\\BotMessages.json', 'r')
botmessages = json.load(botmessagesdata)

version = str(consoletext['WindowVersion'][0])
start = time.time()
Login.BotLogin.variable()

PATH = sys.path[0] + '\\resources\\ConfigData\\Credentials.json'

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    credsfile = io.open(PATH, 'r')
    credentials = json.load(credsfile)
    discord_user_id = str(credentials['ownerid'][0])
    bot_id = str(credentials['botid'][0])
    _logging = str(credentials['logging'][0])
    _logbans = str(credentials['logbans'][0])
    _logunbans = str(credentials['logunbans'][0])
    _logkicks = str(credentials['logkicks'][0])
    _bot_prefix = str(credentials['bot_prefix'][0])
    if _bot_prefix == '':
        _bot_prefix = None
    if _bot_prefix is None:
        print('No Prefix specified in Credentials.json. The Bot cannot continue.')
        sys.exit(2)
    if bot_id == 'None':
        bot_id = None
    if discord_user_id == 'None':
        discord_user_id = None


class BotCore:
    def __init__(self):
        pass

    # noinspection PyPep8Naming,PyUnusedLocal
    class bot:
        """
            This Class is for Internal Use only!!!
        """

        @classmethod
        def changewindowtitle_code(self):
            ctypes.windll.kernel32.SetConsoleTitleW(str(consoletext['WindowName'][0]) + version)

        @classmethod
        def changewindowsize_code(self):
            cmd = "mode con: cols=80 lines=23"
            subprocess.Popen(cmd, shell=True)

        @asyncio.coroutine
        def commands_code(client, message):
            yield from Ignore.BotIgnores.ignore(client, message)
            if message.content.startswith(_bot_prefix + "uptime"):
                if message.author.id in somedict['Users']:
                    return
                else:
                    stop = time.time()
                    seconds = stop - start
                    days = int(((seconds / 60) / 60) / 24)
                    hours = str(int((seconds / 60) / 60 - (days * 24)))
                    minutes = str(int((seconds / 60) % 60))
                    seconds = str(int(seconds % 60))
                    days = str(days)
                    time_001 = str(botmessages['Uptime_command_data'][0]).format(days, hours, minutes, seconds)
                    time_parse = time_001
                    try:
                        yield from client.send_message(message.channel, time_parse)
                    except discord.errors.Forbidden:
                        return
            if message.content.startswith(_bot_prefix + "hlreload"):
                if message.author.id == discord_user_id:
                    desmod_new = message.content.lower()[len(_bot_prefix + 'hlreload '):].strip()
                    _somebool = False
                    desmod = None
                    reload_reason = None
                    if desmod_new.rfind('ignore') is not -1:
                        desmod = 'Ignore'
                        rsn = desmod_new.strip('ignore')
                        if rsn.rfind(' | ') is not -1:
                            reason = rsn.strip(' | ')
                            reload_reason = reason
                            _somebool = True
                        else:
                            reason = None
                            reload_reason = reason
                            _somebool = True
                    if _somebool is True:
                        if desmod_new is not None:
                            if desmod == 'Ignore':
                                try:
                                    rsn = reload_reason
                                    yield from Ignore.BotEvents.high_level_reload_helper(client, message, rsn)
                                    module = sys.modules.get(desmod)
                                    importlib.reload(module)
                                    yield from Ignore.BotEvents.high_level_reload_helper2(client, message)
                                    try:
                                        msgdata = str(botmessages['reload_command_data'][0])
                                        message_data = msgdata + ' Reloaded ' + desmod + '.'
                                        if desmod == 'BotLogs':
                                            if rsn is not None:
                                                message_data = message_data + ' Reason: ' + rsn
                                                yield from client.send_message(message.channel, message_data)
                                            else:
                                                yield from client.send_message(message.channel, message_data)
                                        else:
                                            yield from client.send_message(message.channel, message_data)
                                    except discord.errors.Forbidden:
                                        yield from BotPMError._resolve_send_message_error(client, message)
                                except Exception as e:
                                    reloadexception = str(traceback.format_exc())
                                    try:

                                        reload_data = str(botmessages['reload_command_data'][1]).format(reloadexception)
                                        yield from client.send_message(message.channel, reload_data)
                                    except discord.errors.Forbidden:
                                        yield from BotPMError._resolve_send_message_error(client, message)
                    else:
                        try:
                            yield from client.send_message(message.channel, str(botmessages['reload_command_data'][2]))
                        except discord.errors.Forbidden:
                            yield from BotPMError._resolve_send_message_error(client, message)
                else:
                    try:
                        yield from client.send_message(message.channel, str(botmessages['reload_command_data'][3]))
                    except discord.errors.Forbidden:
                        yield from BotPMError._resolve_send_message_error(client, message)

        @classmethod
        @asyncio.coroutine
        def deletemessage_code(self, client, message):
            yield from Ignore.BotEvents._resolve_delete_method(client, message)

        @classmethod
        @asyncio.coroutine
        def editmessage_code(self, client, before, after):
            yield from Ignore.BotEvents._resolve_edit_method(client, before, after)

        @classmethod
        @asyncio.coroutine
        def memberban_code(self, client, member):
            yield from Ignore.BotEvents._resolve_onban(client, member)

        @classmethod
        @asyncio.coroutine
        def memberunban_code(self, client, member):
            yield from Ignore.BotEvents._resolve_onunban(client, member)

        @classmethod
        @asyncio.coroutine
        def memberremove_code(self, client, member):
            yield from Ignore.BotEvents._resolve_onremove(client, member)

        @classmethod
        @asyncio.coroutine
        def memberjoin_code(self, client, member):
            yield from Ignore.BotEvents._resolve_onjoin(client, member)

        @classmethod
        def _login_helper_code(self, client):
            Login.BotLogin.login_info(client)

        @classmethod
        def _discord_logger_code(self):
            Ignore.BotEvents._resolve_discord_logger()

        @classmethod
        def _asyncio_logger_code(self):
            Ignore.BotEvents._resolve_asyncio_logger()

        @classmethod
        @asyncio.coroutine
        def _server_available_code(self, server):
            yield from Ignore.BotEvents.server_available(server)

        @classmethod
        @asyncio.coroutine
        def _server_unavailable_code(self, server):
            yield from Ignore.BotEvents.server_unavailable(server)

        @classmethod
        @asyncio.coroutine
        def _bot_ready_code(self, client):
            yield from Login.BotLogin.on_login(client)
            yield from Ignore.BotEvents._resolve_on_login_voice_channel_join(client)

    @classmethod
    def changewindowtitle(self):
        self.bot.changewindowtitle_code()

    @classmethod
    def changewindowsize(self):
        self.bot.changewindowsize_code()

    @classmethod
    @asyncio.coroutine
    def commands(self, client, message):
        yield from self.bot.commands_code(client, message)

    @classmethod
    @asyncio.coroutine
    def deletemessage(self, client, message):
        yield from self.bot.deletemessage_code(client, message)

    @classmethod
    @asyncio.coroutine
    def editmessage(self, client, before, after):
        yield from self.bot.editmessage_code(client, before, after)

    @classmethod
    @asyncio.coroutine
    def memberban(self, client, member):
        yield from self.bot.memberban_code(client, member)

    @classmethod
    @asyncio.coroutine
    def memberunban(self, client, member):
        yield from self.bot.memberunban_code(client, member)

    @classmethod
    @asyncio.coroutine
    def memberremove(self, client, member):
        yield from self.bot.memberremove_code(client, member)

    @classmethod
    @asyncio.coroutine
    def memberjoin(self, client, member):
        yield from self.bot.memberjoin_code(client, member)

    @classmethod
    def _login_helper(self, client):
        self.bot._login_helper_code(client)

    @classmethod
    def _discord_logger(self):
        self.bot._discord_logger_code()

    @classmethod
    def _asyncio_logger(self):
        self.bot._asyncio_logger_code()

    @classmethod
    @asyncio.coroutine
    def _server_available(self, server):
        yield from self.bot._server_available_code(server)

    @classmethod
    @asyncio.coroutine
    def _server_unavailable(self, server):
        yield from self.bot._server_unavailable_code(server)

    @classmethod
    @asyncio.coroutine
    def _bot_ready(self, client):
        yield from self.bot._bot_ready_code(client)
