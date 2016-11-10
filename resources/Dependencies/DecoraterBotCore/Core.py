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
import os
import discord
from discord.state import ConnectionState
from discord.http import HTTPClient
from discord.voice_client import VoiceClient
import ctypes
import sys
import time
import asyncio
import json
import traceback
import importlib
import io
try:
    import Ignore
except ImportError:
    sepa = os.sep
    bits = ctypes.sizeof(ctypes.c_voidp)
    platform = None
    if bits == 4:
        platform = 'x86'
    elif bits == 8:
        platform = 'x64'
    path = sys.path[0]
    if path.find('\\AppData\\Local\\Temp') != -1:
        path = sys.executable.strip(
            'DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(platform, sys.platform,
                                                                                   sys.implementation,
                                                                                   sys.version_info))
    sys.path.append("{0}{1}resources{1}Dependencies{1}DecoraterBotCore".format(path, sepa))
    import Ignore
try:
    import Login
except ImportError:
    print('Some Unknown thing happened which made a critical bot code file unable to be found.')
from .BotErrors import *
try:
    import BotPMError
except ImportError:
    print('Some Unknown thing happened which made a critical bot code file unable to be found.')
import BotConfigReader


class BotData:
    """
        This Class is for Internal Use only!!!
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
        if self.path.find('\\AppData\\Local\\Temp') != -1:
            self.path = sys.executable.strip(
                'DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(self.platform, sys.platform,
                                                                                       sys.implementation,
                                                                                       sys.version_info))
        self.DBLogin = Login.BotLogin()
        self.DBIgnores = Ignore.BotIgnores()
        self.jsonfile = io.open('{0}{1}resources{1}ConfigData{1}BotBanned.json'.format(self.path, self.sepa))
        self.somedict = json.load(self.jsonfile)
        self.jsonfile.close()
        self.consoledatafile = io.open('{0}{1}resources{1}ConfigData{1}ConsoleWindow.json'.format(self.path, self.sepa))
        self.consoletext = json.load(self.consoledatafile)
        self.consoledatafile.close()
        self.botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.json'.format(self.path, self.sepa))
        self.botmessages = json.load(self.botmessagesdata)
        self.botmessagesdata.close()
        self.version = str(self.consoletext['WindowVersion'][0])
        self.start = time.time()
        self.DBLogin.variable()
        self.PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(self.path, self.sepa)
        if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
            self.BotConfig = BotConfigReader.BotConfigVars()
            self.discord_user_id = self.BotConfig.discord_user_id
            if self.discord_user_id == 'None':
                self.discord_user_id = None
            self._logging = self.BotConfig.logging
            self._logbans = self.BotConfig.logbans
            self._logunbans = self.BotConfig.logunbans
            self._logkicks = self.BotConfig.logkicks
            self._bot_prefix = self.BotConfig.bot_prefix
        # For Cionsole Window size. (windows only)
            self.cmd = "mode con: cols=80 lines=23"
        # The platform list I have so far.
        self.reload_ignores_module = False
        if not (sys.platform.startswith('win') or sys.platform.startswith('linux')):
            self.platerrormsg = str(self.consoletext['Unsupported_Platform'][0])
            raise UnsupportedPlatform(self.platerrormsg.format(sys.platform))

    def changewindowtitle_code(self):
        """
        Changes the console's window Title.
        :return: Nothing.
        """
        if not (sys.platform.startswith('linux')):
            ctypes.windll.kernel32.SetConsoleTitleW(str(self.consoletext['WindowName'][0]) + self.version)
        else:
            sys.stdout.write("\x1b]2;{0}\x07".format(str(self.consoletext['WindowName'][0]) + self.version))
            # print('Canno\'t change Console window title for this platform.\nPlease help the Developer with this.')

    def changewindowsize_code(self):
        """
        Changes the Console's size.
        :return: Nothing.
        """
        # the Following is windows only.
        os.system(self.cmd)

    @asyncio.coroutine
    def commands_code(self, client, message):
        """
        Cental place where all Commands are Registered/Created at.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.DBIgnores.ignore(client, message)
        if message.content.startswith(self._bot_prefix + "uptime"):
            if message.author.id in self.somedict['Users']:
                return
            else:
                stop = time.time()
                seconds = stop - self.start
                days = int(((seconds / 60) / 60) / 24)
                hours = str(int((seconds / 60) / 60 - (days * 24)))
                minutes = str(int((seconds / 60) % 60))
                seconds = str(int(seconds % 60))
                days = str(days)
                time_001 = str(self.botmessages['Uptime_command_data'][0]).format(days, hours, minutes, seconds)
                time_parse = time_001
                try:
                    yield from client.send_message(message.channel, time_parse)
                except discord.errors.Forbidden:
                    return
        if message.content.startswith(self._bot_prefix + "hlreload"):
            if message.author.id == self.discord_user_id:
                desmod_new = message.content.lower()[len(self._bot_prefix + 'hlreload '):].strip()
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
                        self.reload_ignores_module = True
                    else:
                        reason = None
                        reload_reason = reason
                        _somebool = True
                        self.reload_ignores_module = True
                if _somebool is True:
                    if desmod_new is not None:
                        if desmod == 'Ignore':
                            try:
                                rsn = reload_reason
                                yield from self.DBIgnores.high_level_reload_helper(client, message, rsn)
                                module = sys.modules.get(desmod)
                                importlib.reload(module)
                                if self.reload_ignores_module:
                                    # This is to refresh the Class initializations with the updated data.
                                    self.DBIgnores = Ignore.BotIgnores()
                                yield from self.DBIgnores.high_level_reload_helper2(client, message)
                                try:
                                    msgdata = str(self.botmessages['reload_command_data'][0])
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
                                    yield from BotPMError.resolve_send_message_error(client, message)
                            except Exception as e:
                                str(e)
                                reloadexception = str(traceback.format_exc())
                                try:
                                    reload_data = str(self.botmessages['reload_command_data'][1]).format(
                                        reloadexception)
                                    yield from client.send_message(message.channel, reload_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    try:
                        yield from client.send_message(message.channel, str(self.botmessages['reload_command_data'][2]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
            else:
                try:
                    yield from client.send_message(message.channel, str(self.botmessages['reload_command_data'][3]))
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def deletemessage_code(self, client, message):
        """
        Bot Event.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_delete_method(client, message)

    @asyncio.coroutine
    def editmessage_code(self, client, before, after):
        """
        Bot Event.
        :param client: Discord Client.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_edit_method(client, before, after)

    @asyncio.coroutine
    def memberban_code(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_onban(client, member)

    @asyncio.coroutine
    def memberunban_code(self, server, member):
        """
        Bot Event.
        :param server: Server.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_onunban(server, member)

    @asyncio.coroutine
    def memberremove_code(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_onremove(client, member)

    @asyncio.coroutine
    def memberjoin_code(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_onjoin(client, member)

    def login_helper_code(self, client):
        """
        Bot Login Helper.
        :param client: Discord client.
        :return: Nothing.
        """
        self.DBLogin.login_info(client)

    def discord_logger_code(self):
        """
        Logger Data.
        :return: Nothing.
        """
        self.DBIgnores.resolve_discord_logger()

    def asyncio_logger_code(self):
        """
        Asyncio Logger.
        :return: Nothing.
        """
        self.DBIgnores.resolve_asyncio_logger()

    @asyncio.coroutine
    def server_available_code(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        yield from self.DBIgnores.server_available(server)

    @asyncio.coroutine
    def server_unavailable_code(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        yield from self.DBIgnores.server_unavailable(server)

    @asyncio.coroutine
    def groupjoin_code(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_ongroupjoin(channel, user)

    @asyncio.coroutine
    def groupremove_code(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_ongroupremove(channel, user)

    @asyncio.coroutine
    def raw_recv_code(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def raw_send_code(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def bot_resumed_code(self):
        """
        Bot Event.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def typing_code(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :param when: Time.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def errors_code(self, event, *args, **kwargs):
        """
        Bot Event.
        :param event: Event.
        :param args: Args.
        :param kwargs: Other Args.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def channeldelete_code(self, channel):
        """
        Bot Event.
        :param channel: Channels.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def voiceupdate_code(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverrolecreate_code(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverroledelete_code(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverroleupdate_code(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverjoin_code(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverremove_code(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverupdate_code(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def channelcreate_code(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def channelupdate_code(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def memberupdate_code(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def bot_ready_code(self, client):
        """
        Bot Event.
        :param client: Discord Client.
        :return: Nothing.
        """
        yield from self.DBLogin.on_login(client)
        yield from self.DBIgnores.resolve_on_login_voice_channel_join(client)


class BotCore:
    """
    Bot Core for the bot's Events.
    """
    def __init__(self):
        self.bot = BotData()

    def changewindowtitle(self):
        """
        Changes the console's window Title.
        :return: Nothing.
        """
        self.bot.changewindowtitle_code()

    def changewindowsize(self):
        """
        Changes the Console's size.
        :return: Nothing.
        """
        self.bot.changewindowsize_code()

    @asyncio.coroutine
    def commands(self, client, message):
        """
        Cental place where all Commands are Registered/Created at.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.commands_code(client, message)

    @asyncio.coroutine
    def deletemessage(self, client, message):
        """
        Bot Event.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.deletemessage_code(client, message)

    @asyncio.coroutine
    def editmessage(self, client, before, after):
        """
        Bot Event.
        :param client: Discord Client.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        yield from self.bot.editmessage_code(client, before, after)

    @asyncio.coroutine
    def memberban(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.bot.memberban_code(client, member)

    @asyncio.coroutine
    def memberunban(self, server, member):
        """
        Bot Event.
        :param server: Server.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.bot.memberunban_code(server, member)

    @asyncio.coroutine
    def memberremove(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.bot.memberremove_code(client, member)

    @asyncio.coroutine
    def memberjoin(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.bot.memberjoin_code(client, member)

    def login_helper(self, client):
        """
        Bot Login Helper.
        :param client: Discord client.
        :return: Nothing.
        """
        self.bot.login_helper_code(client)

    def discord_logger(self):
        """
        Logger Data.
        :return: Nothing.
        """
        self.bot.discord_logger_code()

    def asyncio_logger(self):
        """
        Asyncio Logger.
        :return: Nothing.
        """
        self.bot.asyncio_logger_code()

    @asyncio.coroutine
    def server_available(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        yield from self.bot.server_available_code(server)

    @asyncio.coroutine
    def server_unavailable(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        yield from self.bot.server_unavailable_code(server)

    @asyncio.coroutine
    def groupjoin(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.bot.groupjoin_code(channel, user)

    @asyncio.coroutine
    def groupremove(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.bot.groupremove_code(channel, user)

    @asyncio.coroutine
    def raw_recv(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        yield from self.bot.raw_recv_code(msg)

    @asyncio.coroutine
    def raw_send(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        yield from self.bot.raw_send_code(payload)

    @asyncio.coroutine
    def bot_resumed(self):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from self.bot.bot_resumed_code()

    @asyncio.coroutine
    def typing(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :param when: Time.
        :return: Nothing.
        """
        yield from self.bot.typing_code(channel, user, when)

    @asyncio.coroutine
    def errors(self, event, *args, **kwargs):
        """
        Bot Event.
        :param event: Event.
        :param args: Args.
        :param kwargs: Other Args.
        :return: Nothing.
        """
        yield from self.bot.errors_code(event, *args, **kwargs)

    @asyncio.coroutine
    def channeldelete(self, channel):
        """
        Bot Event.
        :param channel: Channels.
        :return: Nothing.
        """
        yield from self.bot.channeldelete_code(channel)

    @asyncio.coroutine
    def voiceupdate(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        yield from self.bot.voiceupdate_code(before, after)

    @asyncio.coroutine
    def serverrolecreate(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        yield from self.bot.serverrolecreate_code(role)

    @asyncio.coroutine
    def serverroledelete(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        yield from self.bot.serverroledelete_code(role)

    @asyncio.coroutine
    def serverroleupdate(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        yield from self.bot.serverroleupdate_code(before, after)

    @asyncio.coroutine
    def serverjoin(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.bot.serverjoin_code(server)

    @asyncio.coroutine
    def serverremove(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.bot.serverremove_code(server)

    @asyncio.coroutine
    def serverupdate(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        yield from self.bot.serverupdate_code(before, after)

    @asyncio.coroutine
    def channelcreate(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        yield from self.bot.channelcreate_code(channel)

    @asyncio.coroutine
    def channelupdate(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        yield from self.bot.channelupdate_code(before, after)

    @asyncio.coroutine
    def memberupdate(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        yield from self.bot.memberupdate_code(before, after)

    @asyncio.coroutine
    def bot_ready(self, client):
        """
        Bot Event.
        :param client: Discord client.
        :return: Nothing.
        """
        yield from self.bot.bot_ready_code(client)


class BotClient(discord.Client):
    """
    Bot Main client Class.
    This is where the Events are Registered.
    """
    def __init__(self, *, loop=None, **options):
        self.ws = None
        self.email = None
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self._listeners = []
        self.cache_auth = options.get('cache_auth', True)
        self.shard_id = options.get('shard_id')
        self.shard_count = options.get('shard_count')

        max_messages = options.get('max_messages')
        if max_messages is None or max_messages < 100:
            max_messages = 5000

        self.connection = ConnectionState(self.dispatch, self.request_offline_members,
                                          self._syncer, max_messages, loop=self.loop)

        connector = options.pop('connector', None)
        self.http = HTTPClient(connector, loop=self.loop)

        self._closed = asyncio.Event(loop=self.loop)
        self._is_logged_in = asyncio.Event(loop=self.loop)
        self._is_ready = asyncio.Event(loop=self.loop)

        if VoiceClient.warn_nacl:
            VoiceClient.warn_nacl = False
            log.warning("PyNaCl is not installed, voice will NOT be supported")
        # DecoraterBot Nessessities.
        self.DBCore = BotCore()
        self.DBCore.asyncio_logger()
        self.DBCore.discord_logger()
        self.DBCore.changewindowtitle()
        # self.DBCore.changewindowsize()
        self.DBCore.login_helper(self)

    @asyncio.coroutine
    def on_message(self, message):
        """
        Bo9t Event.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.DBCore.commands(self, message)

    @asyncio.coroutine
    def on_message_delete(self, message):
        """
        Bot Event.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.DBCore.deletemessage(self, message)

    @asyncio.coroutine
    def on_message_edit(self, before, after):
        """
        Bot Event.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        yield from self.DBCore.editmessage(self, before, after)

    @asyncio.coroutine
    def on_channel_delete(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        yield from self.DBCore.channeldelete(channel)

    @asyncio.coroutine
    def on_channel_create(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        yield from self.DBCore.channelcreate(channel)

    @asyncio.coroutine
    def on_channel_update(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        yield from self.DBCore.channelupdate(before, after)

    @asyncio.coroutine
    def on_member_ban(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBCore.memberban(self, member)

    @asyncio.coroutine
    def on_member_unban(self, server, user):
        """
        Bot Event.
        :param server: Server.
        :param user: User.
        :return: Nothing.
        """
        yield from self.DBCore.memberunban(server, user)

    @asyncio.coroutine
    def on_member_remove(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBCore.memberremove(self, member)

    @asyncio.coroutine
    def on_member_update(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        yield from self.DBCore.memberupdate(before, after)

    @asyncio.coroutine
    def on_member_join(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBCore.memberjoin(self, member)

    @asyncio.coroutine
    def on_server_available(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.DBCore.server_available(server)

    @asyncio.coroutine
    def on_server_unavailable(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.DBCore.server_unavailable(server)

    @asyncio.coroutine
    def on_server_join(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.DBCore.serverjoin(server)

    @asyncio.coroutine
    def on_server_remove(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.DBCore.serverremove(server)

    @asyncio.coroutine
    def on_server_update(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        yield from self.DBCore.serverupdate(before, after)

    @asyncio.coroutine
    def on_server_role_create(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        yield from self.DBCore.serverrolecreate(role)

    @asyncio.coroutine
    def on_server_role_delete(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        yield from self.DBCore.serverroledelete(role)

    @asyncio.coroutine
    def on_server_role_update(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        yield from self.DBCore.serverroleupdate(before, after)

    @asyncio.coroutine
    def on_group_join(self, channel, user):
        """
        Bot Event.
        :param channel: Channel.
        :param user: User.
        :return: Nothing.
        """
        yield from self.DBCore.groupjoin(channel, user)

    @asyncio.coroutine
    def on_group_remove(self, channel, user):
        """
        Bot Event.
        :param channel: Channel.
        :param user: User.
        :return: Nothing.
        """
        yield from self.DBCore.groupremove(channel, user)

    @asyncio.coroutine
    def on_error(self, event, *args, **kwargs):
        """
        Bot Event.
        :param event: Event.
        :param args: Args.
        :param kwargs: Other Args.
        :return: Nothing.
        """
        yield from self.DBCore.errors(event, *args, **kwargs)

    @asyncio.coroutine
    def on_voice_state_update(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        yield from self.DBCore.voiceupdate(before, after)

    @asyncio.coroutine
    def on_typing(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channel.
        :param user: User.
        :param when: Time.
        :return: Nothing.
        """
        yield from self.DBCore.typing(channel, user, when)

    @asyncio.coroutine
    def on_socket_raw_receive(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        yield from self.DBCore.raw_recv(msg)

    @asyncio.coroutine
    def on_socket_raw_send(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        yield from self.DBCore.raw_send(payload)

    @asyncio.coroutine
    def on_ready(self):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from self.DBCore.bot_ready(self)

    @asyncio.coroutine
    def on_resumed(self):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from self.DBCore.bot_resumed()
