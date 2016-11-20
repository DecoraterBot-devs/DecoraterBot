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
import json
import traceback
import importlib
import io
try:
    from . import Ignore
except ImportError:
    print('Some Unknown thing happened which made a critical bot code file unable to be found.')
    Ignore = None
try:
    from . import Login
except ImportError:
    print('Some Unknown thing happened which made a critical bot code file unable to be found.')
    Login = None
from .BotErrors import *
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


class BotData(Login.BotLogin):
    """
        This Class is for Internal Use only!!!
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
        self.BotConfig = BotConfigReader.BotConfigVars()
        if self.path.find('\\AppData\\Local\\Temp') != -1:
            self.path = sys.executable.strip(
                'DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(self.platform, sys.platform,
                                                                                       sys.implementation,
                                                                                       sys.version_info))
        self.DBIgnores = Ignore.BotIgnores()
        self.jsonfile = io.open('{0}{1}resources{1}ConfigData{1}BotBanned.json'.format(self.path, self.sepa))
        self.somedict = json.load(self.jsonfile)
        self.jsonfile.close()
        self.consoledatafile = io.open('{0}{1}resources{1}ConfigData{1}ConsoleWindow.{2}.json'.format(
            self.path, self.sepa, self.BotConfig.language))
        self.consoletext = json.load(self.consoledatafile)
        self.consoledatafile.close()
        self.botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.{2}.json'.format(
            self.path, self.sepa, self.BotConfig.language))
        self.botmessages = json.load(self.botmessagesdata)
        self.botmessagesdata.close()
        self.version = str(self.consoletext['WindowVersion'][0])
        self.start = time.time()
        self.variable()
        self.PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(self.path, self.sepa)
        if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
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
            # print('Can not change Console window title for this platform.\nPlease help the Developer with this.')

    def changewindowsize_code(self):
        """
        Changes the Console's size.
        :return: Nothing.
        """
        # the Following is windows only.
        os.system(self.cmd)

    @async
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
                    yield from client.send_message(message.channel, content=time_parse)
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
                                            yield from client.send_message(message.channel, content=message_data)
                                        else:
                                            yield from client.send_message(message.channel, content=message_data)
                                    else:
                                        yield from client.send_message(message.channel, content=message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                            except Exception as e:
                                str(e)
                                reloadexception = str(traceback.format_exc())
                                try:
                                    reload_data = str(self.botmessages['reload_command_data'][1]).format(
                                        reloadexception)
                                    yield from client.send_message(message.channel, content=reload_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    try:
                        yield from client.send_message(message.channel,
                                                       content=str(self.botmessages['reload_command_data'][2]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
            else:
                try:
                    yield from client.send_message(message.channel,
                                                   content=str(self.botmessages['reload_command_data'][3]))
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)

    @async
    def deletemessage_code(self, client, message):
        """
        Bot Event.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_delete_method(client, message)

    @async
    def editmessage_code(self, client, before, after):
        """
        Bot Event.
        :param client: Discord Client.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_edit_method(client, before, after)

    @async
    def memberban_code(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_onban(client, member)

    @async
    def memberunban_code(self, server, member):
        """
        Bot Event.
        :param server: Server.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_onunban(server, member)

    @async
    def memberremove_code(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_onremove(client, member)

    @async
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
        while True:
            ret = self.login_info(client)
            if ret is not None and ret is not -1:
                break

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

    @async
    def server_available_code(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        yield from self.DBIgnores.server_available(server)

    @async
    def server_unavailable_code(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        yield from self.DBIgnores.server_unavailable(server)

    @async
    def groupjoin_code(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_ongroupjoin(channel, user)

    @async
    def groupremove_code(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.DBIgnores.resolve_ongroupremove(channel, user)

    @async
    def raw_recv_code(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def raw_send_code(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def bot_resumed_code(self):
        """
        Bot Event.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
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

    @async
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

    @async
    def channeldelete_code(self, channel):
        """
        Bot Event.
        :param channel: Channels.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def voiceupdate_code(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def serverrolecreate_code(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def serverroledelete_code(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def serverroleupdate_code(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def serverjoin_code(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def serverremove_code(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def serverupdate_code(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def channelcreate_code(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def channelupdate_code(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def memberupdate_code(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @async
    def bot_ready_code(self, client):
        """
        Bot Event.
        :param client: Discord Client.
        :return: Nothing.
        """
        yield from self.on_login(client)
        yield from self.DBIgnores.resolve_on_login_voice_channel_join(client)

    # new events (Since Discord.py v0.13.0+).

    @async
    def serveremojisupdate_code(self, before, after):
        """
        Bot Event.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass


class BotCore(BotData):
    """
    Bot Core for the bot's Events.
    """
    def __init__(self):
        super(BotCore, self).__init__()

    def changewindowtitle(self):
        """
        Changes the console's window Title.
        :return: Nothing.
        """
        self.changewindowtitle_code()

    def changewindowsize(self):
        """
        Changes the Console's size.
        :return: Nothing.
        """
        self.changewindowsize_code()

    @async
    def commands(self, client, message):
        """
        Cental place where all Commands are Registered/Created at.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.commands_code(client, message)

    @async
    def deletemessage(self, client, message):
        """
        Bot Event.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.deletemessage_code(client, message)

    @async
    def editmessage(self, client, before, after):
        """
        Bot Event.
        :param client: Discord Client.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        yield from self.editmessage_code(client, before, after)

    @async
    def memberban(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.memberban_code(client, member)

    @async
    def memberunban(self, server, member):
        """
        Bot Event.
        :param server: Server.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.memberunban_code(server, member)

    @async
    def memberremove(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.memberremove_code(client, member)

    @async
    def memberjoin(self, client, member):
        """
        Bot Event.
        :param client: Discord Client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.memberjoin_code(client, member)

    def login_helper(self, client):
        """
        Bot Login Helper.
        :param client: Discord client.
        :return: Nothing.
        """
        self.login_helper_code(client)

    def discord_logger(self):
        """
        Logger Data.
        :return: Nothing.
        """
        self.discord_logger_code()

    def asyncio_logger(self):
        """
        Asyncio Logger.
        :return: Nothing.
        """
        self.asyncio_logger_code()

    @async
    def server_available(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        yield from self.server_available_code(server)

    @async
    def server_unavailable(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        yield from self.server_unavailable_code(server)

    @async
    def groupjoin(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.groupjoin_code(channel, user)

    @async
    def groupremove(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.groupremove_code(channel, user)

    @async
    def raw_recv(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        yield from self.raw_recv_code(msg)

    @async
    def raw_send(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        yield from self.raw_send_code(payload)

    @async
    def bot_resumed(self):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from self.bot_resumed_code()

    @async
    def typing(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :param when: Time.
        :return: Nothing.
        """
        yield from self.typing_code(channel, user, when)

    @async
    def errors(self, event, *args, **kwargs):
        """
        Bot Event.
        :param event: Event.
        :param args: Args.
        :param kwargs: Other Args.
        :return: Nothing.
        """
        yield from self.errors_code(event, *args, **kwargs)

    @async
    def channeldelete(self, channel):
        """
        Bot Event.
        :param channel: Channels.
        :return: Nothing.
        """
        yield from self.channeldelete_code(channel)

    @async
    def voiceupdate(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        yield from self.voiceupdate_code(before, after)

    @async
    def serverrolecreate(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        yield from self.serverrolecreate_code(role)

    @async
    def serverroledelete(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        yield from self.serverroledelete_code(role)

    @async
    def serverroleupdate(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        yield from self.serverroleupdate_code(before, after)

    @async
    def serverjoin(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.serverjoin_code(server)

    @async
    def serverremove(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.serverremove_code(server)

    @async
    def serverupdate(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        yield from self.serverupdate_code(before, after)

    @async
    def channelcreate(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        yield from self.channelcreate_code(channel)

    @async
    def channelupdate(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        yield from self.channelupdate_code(before, after)

    @async
    def memberupdate(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        yield from self.memberupdate_code(before, after)

    @async
    def bot_ready(self, client):
        """
        Bot Event.
        :param client: Discord client.
        :return: Nothing.
        """
        yield from self.bot_ready_code(client)

    # new events (Since Discord.py v0.13.0+).

    @async
    def serveremojisupdate(self, before, after):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from self.serveremojisupdate_code(before, after)


class BotClient(discord.Client):
    """
    Bot Main client Class.
    This is where the Events are Registered.
    """
    def __init__(self, *, loop=None, **options):
        # Execute Overridden __init__() function.
        super(BotClient, self).__init__(loop=loop, **options)
        # DecoraterBot Nessessities.
        self.DBCore = BotCore()
        self.DBCore.asyncio_logger()
        self.DBCore.discord_logger()
        self.DBCore.changewindowtitle()
        # self.DBCore.changewindowsize()
        self.DBCore.login_helper(self)

    @async
    def on_message(self, message):
        """
        Bot Event.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.DBCore.commands(self, message)

    @async
    def on_message_delete(self, message):
        """
        Bot Event.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.DBCore.deletemessage(self, message)

    @async
    def on_message_edit(self, before, after):
        """
        Bot Event.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        yield from self.DBCore.editmessage(self, before, after)

    @async
    def on_channel_delete(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        yield from self.DBCore.channeldelete(channel)

    @async
    def on_channel_create(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        yield from self.DBCore.channelcreate(channel)

    @async
    def on_channel_update(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        yield from self.DBCore.channelupdate(before, after)

    @async
    def on_member_ban(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBCore.memberban(self, member)

    @async
    def on_member_unban(self, server, user):
        """
        Bot Event.
        :param server: Server.
        :param user: User.
        :return: Nothing.
        """
        yield from self.DBCore.memberunban(server, user)

    @async
    def on_member_remove(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBCore.memberremove(self, member)

    @async
    def on_member_update(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        yield from self.DBCore.memberupdate(before, after)

    @async
    def on_member_join(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.DBCore.memberjoin(self, member)

    @async
    def on_server_available(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.DBCore.server_available(server)

    @async
    def on_server_unavailable(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.DBCore.server_unavailable(server)

    @async
    def on_server_join(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.DBCore.serverjoin(server)

    @async
    def on_server_remove(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.DBCore.serverremove(server)

    @async
    def on_server_update(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        yield from self.DBCore.serverupdate(before, after)

    @async
    def on_server_role_create(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        yield from self.DBCore.serverrolecreate(role)

    @async
    def on_server_role_delete(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        yield from self.DBCore.serverroledelete(role)

    @async
    def on_server_role_update(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        yield from self.DBCore.serverroleupdate(before, after)

    @async
    def on_group_join(self, channel, user):
        """
        Bot Event.
        :param channel: Channel.
        :param user: User.
        :return: Nothing.
        """
        yield from self.DBCore.groupjoin(channel, user)

    @async
    def on_group_remove(self, channel, user):
        """
        Bot Event.
        :param channel: Channel.
        :param user: User.
        :return: Nothing.
        """
        yield from self.DBCore.groupremove(channel, user)

    @async
    def on_error(self, event, *args, **kwargs):
        """
        Bot Event.
        :param event: Event.
        :param args: Args.
        :param kwargs: Other Args.
        :return: Nothing.
        """
        yield from self.DBCore.errors(event, *args, **kwargs)

    @async
    def on_voice_state_update(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        yield from self.DBCore.voiceupdate(before, after)

    @async
    def on_typing(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channel.
        :param user: User.
        :param when: Time.
        :return: Nothing.
        """
        yield from self.DBCore.typing(channel, user, when)

    @async
    def on_socket_raw_receive(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        yield from self.DBCore.raw_recv(msg)

    @async
    def on_socket_raw_send(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        yield from self.DBCore.raw_send(payload)

    @async
    def on_ready(self):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from self.DBCore.bot_ready(self)

    @async
    def on_resumed(self):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from self.DBCore.bot_resumed()

    # new events (Since Discord.py v0.13.0+).

    @async
    def on_server_emojis_update(self, before, after):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from self.serveremojisupdate(before, after)

    @async
    def on_reaction_add(self, reaction, user):
        """
        Bot Event.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_reaction_remove(self, reaction, user):
        """
        Bot Event.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass
