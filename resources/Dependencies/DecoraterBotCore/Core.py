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
    if bits == 4:
        platform = 'x86'
    elif bits == 8:
        platform = 'x64'
    path = sys.path[0]
    if path.find('\\AppData\\Local\\Temp') != -1:
        path = sys.executable.strip('DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(platform, sys.platform, sys.implementation, sys.version_info))
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

sepa = os.sep
bits = ctypes.sizeof(ctypes.c_voidp)
if bits == 4:
    platform = 'x86'
elif bits == 8:
    platform = 'x64'
path = sys.path[0]
if path.find('\\AppData\\Local\\Temp') != -1:
    path = sys.executable.strip('DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(platform, sys.platform, sys.implementation, sys.version_info))

DBLogin = Login.BotLogin()
DBEvents = Ignore.BotEvents()
DBIgnores = Ignore.BotIgnores()
jsonfile = io.open('{0}{1}resources{1}ConfigData{1}BotBanned.json'.format(path, sepa))
somedict = json.load(jsonfile)
jsonfile.close()
consoledatafile = io.open('{0}{1}resources{1}ConfigData{1}ConsoleWindow.json'.format(path, sepa))
consoletext = json.load(consoledatafile)
consoledatafile.close()
botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.json'.format(path, sepa))
botmessages = json.load(botmessagesdata)
botmessagesdata.close()

version = str(consoletext['WindowVersion'][0])
start = time.time()
DBLogin.variable()

PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(path, sepa)

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    BotConfig = BotConfigReader.BotConfigVars()
    discord_user_id = BotConfig.discord_user_id
    if discord_user_id == 'None':
        discord_user_id = None
    _logging = BotConfig.logging
    _logbans = BotConfig.logbans
    _logunbans = BotConfig.logunbans
    _logkicks = BotConfig.logkicks
    _bot_prefix = BotConfig.bot_prefix

# The platform list I have so far.
if not (sys.platform.startswith('win') or sys.platform.startswith('linux')):
    platerrormsg = str(consoletext['Unsupported_Platform'][0])
    raise UnsupportedPlatform(platerrormsg.format(sys.platform))


class BotData:
    """
        This Class is for Internal Use only!!!
    """
    def __init__(self):
        pass

    @staticmethod
    def changewindowtitle_code():
        """
        Changes the console's window Title.
        :return: Nothing.
        """
        # the Following is windows only.
        if not (sys.platform.startswith('linux')):
            ctypes.windll.kernel32.SetConsoleTitleW(str(consoletext['WindowName'][0]) + version)
        else:
            sys.stdout.write("\x1b]2;{0}\x07".format(str(consoletext['WindowName'][0]) + version))
            # print('Canno\'t change Console window title for this platform.\nPlease help the Developer with this.')

    @staticmethod
    def changewindowsize_code():
        """
        Changes the Console's size.
        :return: Nothing.
        """
        # the Following is windows only.
        cmd = "mode con: cols=80 lines=23"
        os.system(cmd)

    @asyncio.coroutine
    def commands_code(self, client, message):
        """
        Cental place where all Commands are Registered/Created at.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from DBIgnores.ignore(client, message)
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
                                yield from DBEvents.high_level_reload_helper(client, message, rsn)
                                module = sys.modules.get(desmod)
                                importlib.reload(module)
                                yield from DBEvents.high_level_reload_helper2(client, message)
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
                                    yield from BotPMError.resolve_send_message_error(client, message)
                            except Exception as e:
                                str(e)
                                reloadexception = str(traceback.format_exc())
                                try:
                                    reload_data = str(botmessages['reload_command_data'][1]).format(reloadexception)
                                    yield from client.send_message(message.channel, reload_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    try:
                        yield from client.send_message(message.channel, str(botmessages['reload_command_data'][2]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
            else:
                try:
                    yield from client.send_message(message.channel, str(botmessages['reload_command_data'][3]))
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
        yield from DBEvents.resolve_delete_method(client, message)

    @asyncio.coroutine
    def editmessage_code(self, client, before, after):
        """
        Bot Event.
        :param client: Discord Client.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        yield from DBEvents.resolve_edit_method(client, before, after)

    @asyncio.coroutine
    def memberban_code(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from DBEvents.resolve_onban(client, member)

    @asyncio.coroutine
    def memberunban_code(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from DBEvents.resolve_onunban(client, member)

    @asyncio.coroutine
    def memberremove_code(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from DBEvents.resolve_onremove(client, member)

    @asyncio.coroutine
    def memberjoin_code(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from DBEvents.resolve_onjoin(client, member)

    @staticmethod
    def login_helper_code(client):
        """
        Bot Login Helper.
        :param client: Discord client.
        :return: Nothing.
        """
        DBLogin.login_info(client)

    @staticmethod
    def discord_logger_code():
        """
        Logger Data.
        :return: Nothing.
        """
        DBEvents.resolve_discord_logger()

    @staticmethod
    def asyncio_logger_code():
        """
        Asyncio Logger.
        :return: Nothing.
        """
        DBEvents.resolve_asyncio_logger()

    @asyncio.coroutine
    def server_available_code(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        yield from DBEvents.server_available(server)

    @asyncio.coroutine
    def server_unavailable_code(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        yield from DBEvents.server_unavailable(server)

    @asyncio.coroutine
    def groupjoin_code(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from DBEvents.resolve_ongroupjoin(channel, user)

    @asyncio.coroutine
    def groupremove_code(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from DBEvents.resolve_ongroupremove(channel, user)

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
        yield from DBLogin.on_login(client)
        yield from DBEvents.resolve_on_login_voice_channel_join(client)


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
    def memberunban(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.bot.memberunban_code(client, member)

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


DBCore = BotCore()


class BotClient(discord.Client):
    """
    Bot Main client Class.
    This is where the Events are Registered.
    """
    # Hack to not overwrite the __init__ function in discord.Client()
    # This is required to actually login and run the bot or you will be screwed. DO NOT REMOVE THIS HACK!!!
    def not_a_async_function(self):
        """
        This is a bypass for overloading the __init__ function in Discord.py
        which would be bad as then the bot would not be able to connect.
        :return: Nothing.
        """
        DBCore.asyncio_logger()
        DBCore.discord_logger()
        DBCore.changewindowtitle()
        # DBCore.changewindowsize()
        DBCore.login_helper(self)

    @asyncio.coroutine
    def on_message(self, message):
        """
        Bo9t Event.
        :param message: Messages.
        :return: Nothing.
        """
        yield from DBCore.commands(self, message)

    @asyncio.coroutine
    def on_message_delete(self, message):
        """
        Bot Event.
        :param message: Messages.
        :return: Nothing.
        """
        yield from DBCore.deletemessage(self, message)

    @asyncio.coroutine
    def on_message_edit(self, before, after):
        """
        Bot Event.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        yield from DBCore.editmessage(self, before, after)

    @asyncio.coroutine
    def on_channel_delete(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        yield from DBCore.channeldelete(channel)

    @asyncio.coroutine
    def on_channel_create(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        yield from DBCore.channelcreate(channel)

    @asyncio.coroutine
    def on_channel_update(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        yield from DBCore.channelupdate(before, after)

    @asyncio.coroutine
    def on_member_ban(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        yield from DBCore.memberban(self, member)

    @asyncio.coroutine
    def on_member_unban(self, server, user):
        """
        Bot Event.
        :param server: Server.
        :param user: User.
        :return: Nothing.
        """
        yield from DBCore.memberunban(server, user)

    @asyncio.coroutine
    def on_member_remove(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        yield from DBCore.memberremove(self, member)

    @asyncio.coroutine
    def on_member_update(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        yield from DBCore.memberupdate(before, after)

    @asyncio.coroutine
    def on_member_join(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        yield from DBCore.memberjoin(self, member)

    @asyncio.coroutine
    def on_server_available(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from DBCore.server_available(server)

    @asyncio.coroutine
    def on_server_unavailable(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from DBCore.server_unavailable(server)

    @asyncio.coroutine
    def on_server_join(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from DBCore.serverjoin(server)

    @asyncio.coroutine
    def on_server_remove(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from DBCore.serverremove(server)

    @asyncio.coroutine
    def on_server_update(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        yield from DBCore.serverupdate(before, after)

    @asyncio.coroutine
    def on_server_role_create(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        yield from DBCore.serverrolecreate(role)

    @asyncio.coroutine
    def on_server_role_delete(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        yield from DBCore.serverroledelete(role)

    @asyncio.coroutine
    def on_server_role_update(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        yield from DBCore.serverroleupdate(before, after)

    @asyncio.coroutine
    def on_group_join(self, channel, user):
        """
        Bot Event.
        :param channel: Channel.
        :param user: User.
        :return: Nothing.
        """
        yield from DBCore.groupjoin(channel, user)

    @asyncio.coroutine
    def on_group_remove(self, channel, user):
        """
        Bot Event.
        :param channel: Channel.
        :param user: User.
        :return: Nothing.
        """
        yield from DBCore.groupremove(channel, user)

    @asyncio.coroutine
    def on_error(self, event, *args, **kwargs):
        """
        Bot Event.
        :param event: Event.
        :param args: Args.
        :param kwargs: Other Args.
        :return: Nothing.
        """
        yield from DBCore.errors(event, *args, **kwargs)

    @asyncio.coroutine
    def on_voice_state_update(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        yield from DBCore.voiceupdate(before, after)

    @asyncio.coroutine
    def on_typing(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channel.
        :param user: User.
        :param when: Time.
        :return: Nothing.
        """
        yield from DBCore.typing(channel, user, when)

    @asyncio.coroutine
    def on_socket_raw_receive(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        yield from DBCore.raw_recv(msg)

    @asyncio.coroutine
    def on_socket_raw_send(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        yield from DBCore.raw_send(payload)

    @asyncio.coroutine
    def on_ready(self):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from DBCore.bot_ready(self)

    @asyncio.coroutine
    def on_resumed(self):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from DBCore.bot_resumed()
