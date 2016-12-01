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
import os.path
import ctypes
import sys
import aiohttp
import discord
from discord.ext import commands
import time
import json
import traceback
import io
from .BotErrors import *
try:
    from . import BotPMError
except ImportError:
    print('Some Unknown thing happened which made a critical bot code file unable to be found.')
    BotPMError = None
from . import BotConfigReader
from .BotLogs import *
from sasync import *
import asyncio
from . import containers
from colorama import Fore, Back, Style
from colorama import init
from discord.__init__ import __version__

__all__ = ['main', 'BotClient']

config = BotConfigReader.BotConfigVars()


class BotClient(commands.Bot):
    """
    Bot Main client Class.
    This is where the Events are Registered.
    """
    def __init__(self, **kwargs):
        self.BotConfig = config
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
        self.botbanslist = io.open('{0}{1}resources{1}ConfigData{1}BotBanned.json'.format(self.path, self.sepa))
        self.banlist = json.load(self.botbanslist)
        self.botbanslist.close()
        self.consoledatafile = io.open('{0}{1}resources{1}ConfigData{1}ConsoleWindow.{2}.json'.format(
            self.path, self.sepa, self.BotConfig.language))
        self.consoletext = json.load(self.consoledatafile)
        self.consoledatafile.close()
        try:
            self.ignoreslistfile = io.open('{0}{1}resources{1}ConfigData{1}IgnoreList.json'.format(
                self.path, self.sepa))
            self.ignoreslist = json.load(self.ignoreslistfile)
            self.ignoreslistfile.close()
        except FileNotFoundError:
            print(str(self.consoletext['Missing_JSON_Errors'][0]))
            sys.exit(2)
        self.botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.{2}.json'.format(
            self.path, self.sepa, self.BotConfig.language))
        self.botmessages = json.load(self.botmessagesdata)
        self.botmessagesdata.close()
        try:
            self.commandslist = io.open('{0}{1}resources{1}ConfigData{1}BotCommands.json'.format(self.path,
                                                                                                 self.sepa))
            self.commandlist = json.load(self.commandslist)
            self.commandslist.close()
        except FileNotFoundError:
            print(str(self.consoletext['Missing_JSON_Errors'][3]))
            sys.exit(2)
        self.version = str(self.consoletext['WindowVersion'][0])
        self.start = time.time()
        # default to True in case options are not present in Credentials.json
        self.reconnects = 0
        self.is_bot_logged_in = False
        self.logged_in = False
        self.discord_user_email = None
        self.owner_id = None
        self.discord_user_password = None
        self.bot_token = None
        self.logging = True
        self.pm_commands_list = True
        self.logbans = True
        self.logunbans = True
        self.logkicks = True
        self.discord_logger_ = True
        self.asyncio_logger_ = True
        self.log_available = True
        self.log_unavailable = True
        self.log_channel_create = True
        self.log_channel_delete = True
        self.log_channel_update = True
        self.log_member_update = True
        self.log_server_join = True
        self.log_ytdl = True
        self.log_server_remove = True
        self.log_server_update = True
        self.log_server_role_create = True
        self.log_server_role_delete = True
        self.log_server_role_update = True
        self.pm_command_errors = True
        self.is_official_bot = True
        self.log_group_join = True
        self.log_group_remove = True
        self.log_error = True
        self.log_voice_state_update = True
        self.log_typing = True
        self.log_socket_raw_receive = True
        self.log_socket_raw_send = True
        self.log_resumed = True
        self.log_member_join = True
        self.log_games = True
        self.bot_prefix = ''
        # Will Always be True to prevent the Error Handler from Causing Issues later.
        # Well only if the PM Error handler is False.
        self.enable_error_handler = True
        self.PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(self.path, self.sepa)
        if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
            self.discord_user_email = self.BotConfig.discord_user_email
            self.discord_user_password = self.BotConfig.discord_user_password
            self.bot_token = self.BotConfig.bot_token
            self.pm_commands_list = self.BotConfig.pm_commands_list
            if self.discord_user_email == 'None':
                self.discord_user_email = None
            if self.discord_user_password == 'None':
                self.discord_user_password = None
            if self.bot_token == 'None':
                self.bot_token = None
            if self.is_bot_logged_in:
                self.is_bot_logged_in = False
            self.discord_user_id = self.BotConfig.discord_user_id
            if self.discord_user_id == 'None':
                self.discord_user_id = None
            self.owner_id = self.discord_user_id
            self.logging = self.BotConfig.logging
            self.logbans = self.BotConfig.logbans
            self.log_ytdl = self.BotConfig.log_ytdl
            self.logunbans = self.BotConfig.logunbans
            self.logkicks = self.BotConfig.logkicks
            self.bot_prefix = self.BotConfig.bot_prefix
            if self.bot_prefix == '':
                self.bot_prefix = None
            if self.bot_prefix is None:
                print('No Prefix specified in Credentials.json. The Bot cannot continue.')
                sys.exit(2)
            self.disable_voice_commands = self.BotConfig.disable_voice_commands
            self.pm_command_errors = self.BotConfig.pm_command_errors
            self.discord_logger_ = self.BotConfig.discord_logger
            self.asyncio_logger_ = self.BotConfig.asyncio_logger
            self.log_available = self.BotConfig.log_available
            self.log_unavailable = self.BotConfig.log_unavailable
            self.log_channel_create = self.BotConfig.log_channel_create
            self.log_channel_delete = self.BotConfig.log_channel_delete
            self.log_channel_update = self.BotConfig.log_channel_update
            self.log_member_update = self.BotConfig.log_member_update
            self.is_official_bot = self.BotConfig.is_official_bot
            self.log_server_join = self.BotConfig.log_server_join
            self.log_server_remove = self.BotConfig.log_server_remove
            self.log_server_update = self.BotConfig.log_server_update
            self.log_server_role_create = self.BotConfig.log_server_role_create
            self.log_server_role_delete = self.BotConfig.log_server_role_delete
            self.log_server_role_update = self.BotConfig.log_server_role_update
            self.log_group_join = self.BotConfig.log_group_join
            self.log_group_remove = self.BotConfig.log_group_remove
            self.log_error = self.BotConfig.log_error
            self.log_voice_state_update = self.BotConfig.log_voice_state_update
            self.log_typing = self.BotConfig.log_typing
            self.log_socket_raw_receive = self.BotConfig.log_socket_raw_receive
            self.log_socket_raw_send = self.BotConfig.log_socket_raw_send
            self.log_resumed = self.BotConfig.log_resumed
            self.log_member_join = self.BotConfig.log_member_join
            self.log_games = self.BotConfig.log_games
        if (self.logging or self.logbans or self.logunbans or self.logkicks or self.discord_logger_ or
                self.asyncio_logger_ or self.log_available or self.log_unavailable or self.log_channel_create or
                self.log_channel_delete or self.log_channel_update or self.log_member_update or self.log_server_join or
                self.log_server_remove or self.log_server_update or self.log_server_role_create or
                self.log_server_role_delete or self.log_server_role_update or self.log_group_join or
                self.log_group_remove or self.log_error or self.log_voice_state_update or self.log_typing or
                self.log_socket_raw_receive or self.log_socket_raw_send or self.log_resumed or self.log_member_join or
                self.enable_error_handler or self.log_games or self.log_ytdl):
            self.DBLogs = BotLogger()
        self.somebool = False
        self.reload_normal_commands = False
        self.reload_voice_commands = False
        self.reload_reason = None
        self.desmod = None
        self.desmod_new = None
        self.rejoin_after_reload = False
        # For Console Window size. (windows only)
        self.cmd = "mode con: cols=80 lines=23"
        # The platform list I have so far.
        if not (sys.platform.startswith('win') or sys.platform.startswith('linux')):
            self.platerrormsg = str(self.consoletext['Unsupported_Platform'][0])
            raise UnsupportedPlatform(self.platerrormsg.format(sys.platform))
        # DecoraterBot Necessities.
        self.asyncio_logger()
        self.discord_logger()
        self.changewindowtitle()
        # self.changewindowsize()
        super(BotClient, self).__init__(**kwargs)
        self.initial_commands_cogs = [
            'botcorecommands',
            'botcommands',
            'botvoicecommands'
        ]
        for commands_cog in self.initial_commands_cogs:
            ret = containers.load_command(self, commands_cog)
            if type(ret) == str:
                print(ret)
        self.remove_command("help")
        init()
        self.variable()
        self.login_helper()  # handles login.

    def changewindowtitle(self):
        """
        Changes the console's window Title.
        :return: Nothing.
        """
        if sys.platform.startswith('win'):
            ctypes.windll.kernel32.SetConsoleTitleW(str(self.consoletext['WindowName'][0]) + self.version)
        elif sys.platform.startswith('linux'):
            sys.stdout.write("\x1b]2;{0}\x07".format(str(self.consoletext['WindowName'][0]) + self.version))
        else:
            print('Can not change Console window title for this platform.\nPlease help the Developer with this.')

    def changewindowsize(self):
        """
        Changes the Console's size.
        :return: Nothing.
        """
        # the Following is windows only.
        os.system(self.cmd)

    def discord_logger(self):
        """
        Logger Data.
        :return: Nothing.
        """
        if self.discord_logger_:
            self.DBLogs.set_up_discord_logger()

    def asyncio_logger(self):
        """
        Asyncio Logger.
        :return: Nothing.
        """
        if self.asyncio_logger_:
            self.DBLogs.set_up_asyncio_logger(bot=self)

    @async
    def on_message(self, message):
        """
        Bot Event.
        :param message: Messages.
        :return: Nothing.
        """
        if self.user.mention in message.content:
            yield from self.bot_mentioned_helper(message)
        if len(message.mentions) > 5:
            yield from self.mention_ban_helper(message)
        if message.channel.is_private:
            if self.is_official_bot:
                if message.content.startswith('https://discord.gg/'):
                    yield from self.send_message(message.channel,
                                                 content=str(self.botmessages['join_command_data'][3]))
                if message.content.startswith('http://discord.gg/'):
                    yield from self.send_message(message.channel,
                                                 content=str(self.botmessages['join_command_data'][3]))
        yield from self.process_commands(message)

    @async
    def on_message_delete(self, message):
        """
        Bot Event.
        :param message: Message.
        :return: Nothing.
        """
        try:
            if message.channel.is_private is not False:
                if self.logging:
                    self.DBLogs.delete_logs(message)
            elif message.channel.server and message.channel.server.id == "81812480254291968":
                if message.author.id == self.user.id:
                    return
                elif message.channel.id == "153055192873566208":
                    return
                elif message.channel.id == "87382611688689664":
                    return
                else:
                    yield from self.DBLogs.send_delete_logs(self, message)
            else:
                if message.channel.is_private is not False:
                    return
                elif message.channel.server.id == '95342850102796288':
                    return
                else:
                    if self.logging:
                        self.DBLogs.delete_logs(message)
        except Exception as e:
            funcname = 'on_message_delete'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @async
    def on_message_edit(self, before, after):
        """
        Bot Event.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        try:
            if before.channel.is_private is not False:
                if self.logging:
                    self.DBLogs.edit_logs(before, after)
            elif before.channel.server and before.channel.server.id == "81812480254291968":
                if before.author.id == self.user.id:
                    return
                elif before.channel.id == "153055192873566208":
                    return
                elif before.channel.id == "87382611688689664":
                    return
                else:
                    yield from self.DBLogs.send_edit_logs(self, before, after)
            else:
                if before.channel.is_private is not False:
                    return
                elif before.channel.server.id == '95342850102796288':
                    return
                else:
                    if self.logging:
                        self.DBLogs.edit_logs(before, after)
        except Exception as e:
            funcname = 'on_message_edit'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @async
    def on_channel_delete(self, channel):
        """
        Bot Event.
        :param channel: Channels.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_channel_create(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_channel_update(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_member_ban(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            if self.logbans:
                yield from self.DBLogs.onban(member)
            if member.server and member.server.id == "71324306319093760":
                yield from self.verify_cache_cleanup(member)
        except Exception as e:
            funcname = 'on_member_ban'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @async
    def on_member_unban(self, server, user):
        """
        Bot Event.
        :param server: Server.
        :param user: User.
        :return: Nothing.
        """
        try:
            if self.logunbans:
                yield from self.DBLogs.onunban(server, user)
        except Exception as e:
            funcname = 'on_member_unban'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @async
    def on_member_remove(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            try:
                banslist = yield from self.get_bans(member.server)
                if member in banslist:
                    return
                else:
                    if self.logkicks:
                        yield from self.DBLogs.onkick(member)
            except (discord.errors.HTTPException, discord.errors.Forbidden):
                if self.logkicks:
                    yield from self.DBLogs.onkick(member)
            if member.server and member.server.id == "71324306319093760":
                yield from self.verify_cache_cleanup_2(self, member)
        except Exception as e:
            funcname = 'on_member_remove'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @async
    def on_member_update(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_member_join(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            # TODO: Add logging for this.
            if member.server.id == '71324306319093760' and member.bot is not True:
                file_path_join_1 = '{0}resources{0}ConfigData{0}serverconfigs{0}'.format(self.sepa)
                filename_join_1 = 'servers.json'
                serveridslistfile = io.open(self.path + file_path_join_1 + filename_join_1)
                serveridslist = json.load(serveridslistfile)
                serveridslistfile.close()
                serverid = str(serveridslist['config_server_ids'][0])
                file_path_join_2 = '{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}verifications{0}'.format(
                    self.sepa, serverid)
                filename_join_2 = 'verifymessages.json'
                filename_join_3 = 'verifycache.json'
                filename_join_4 = 'verifycache.json'
                memberjoinmessagedatafile = io.open(self.path + file_path_join_2 + filename_join_2)
                memberjoinmessagedata = json.load(memberjoinmessagedatafile)
                memberjoinmessagedatafile.close()
                msg_info = str(memberjoinmessagedata['verify_messages'][0])
                message_data = msg_info.format(member.id, member.server.name)
                des_channel = str(memberjoinmessagedata['verify_messages_channel'][0])
                joinedlistfile = io.open(self.path + file_path_join_2 + filename_join_3)
                newlyjoinedlist = json.load(joinedlistfile)
                joinedlistfile.close()
                yield from self.send_message(discord.Object(id=des_channel), content=message_data)
                if member.id in newlyjoinedlist['users_to_be_verified']:
                    # since this person is already in the list lets not readd them.
                    pass
                else:
                    newlyjoinedlist['users_to_be_verified'].append(member.id)
                    json.dump(newlyjoinedlist, open(self.path + file_path_join_2 + filename_join_4, "w"))
        except Exception as e:
            funcname = 'on_member_join'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @async
    def on_server_available(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        if self.log_available:
            yield from self.DBLogs.onavailable(server)

    @async
    def on_server_unavailable(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        if self.log_unavailable:
            yield from self.DBLogs.onunavailable(server)

    @async
    def on_server_join(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_server_remove(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_server_update(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_server_role_create(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_server_role_delete(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_server_role_update(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_group_join(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        try:
            if self.log_group_join:
                yield from self.DBLogs.ongroupjoin(channel, user)
        except Exception as e:
            funcname = 'on_group_join'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @async
    def on_group_remove(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        try:
            if self.log_group_remove:
                yield from self.DBLogs.ongroupremove(channel, user)
        except Exception as e:
            funcname = 'on_group_remove'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @async
    def on_error(self, event, *args, **kwargs):
        """
        Bot Event.
        :param event: Event.
        :param args: Args.
        :param kwargs: Other Args.
        :return: Nothing.
        """
        funcname = event
        tbinfo = str(traceback.format_exc())
        yield from self.DBLogs.on_bot_error(funcname, tbinfo, None)

    @async
    def on_voice_state_update(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_typing(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :param when: Time.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_socket_raw_receive(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_socket_raw_send(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @async
    def on_ready(self):
        """
        Bot Event.
        :return: Nothing.
        """
        yield from self.on_login()
        # try:
        #     if self.disable_voice_commands is not True:
        #         yield from self.DBVoiceCommands.reload_commands_bypass3_new(self)
        #     else:
        #         return
        # except Exception as e:
        #     funcname = 'on_ready'
        #     tbinfo = str(traceback.format_exc())
        #     yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @async
    def on_resumed(self):
        """
        Bot Event.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    # new events (Since Discord.py v0.13.0+).

    @async
    def on_server_emojis_update(self, before, after):
        """
        Bot Event.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    # added in Discord.py v0.14.3.

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

    # added in Discord.py v0.15.0.

    @async
    def on_reaction_clear(self, message, reactions):
        """
        Bot Event.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    # Helpers.

    @async
    def mention_ban_helper(self, message):
        """
        Bot Commands.
        :param message: Messages.
        :return: Nothing.
        """
        if message.author.id == self.user.id:
            return
        if message.channel.server.id == "105010597954871296":
            return
        if message.author.id == self.owner_id:
            return
        else:
            try:
                yield from self.ban(message.author)
                try:
                    message_data = str(self.botmessages['mention_spam_ban'][0]).format(message.author)
                    yield from self.send_message(message.channel, content=message_data)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error_old(self, message)
            except discord.errors.Forbidden:
                try:
                    msgdata = str(self.botmessages['mention_spam_ban'][1]).format(message.author)
                    message_data = msgdata
                    yield from self.send_message(message.channel, content=message_data)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error_old(self, message)
            except discord.HTTPException:
                try:
                    msgdata = str(self.botmessages['mention_spam_ban'][2]).format(message.author)
                    message_data = msgdata
                    yield from self.send_message(message.channel, content=message_data)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error_old(self, message)

    @async
    def bot_mentioned_helper(self, message):
        """
        Bot Commands.
        :param message: Messages.
        :return: Nothing.
        """
        if message.author.id in self.banlist['Users']:
            return
        elif message.author.bot:
            return
        else:
            pref = self.bot_prefix
            unig = 'unignorechannel'
            # Allows Joining a Voice Channel.
            # This is handling if some idiot mentions the bot with this command in it.
            # This also bypasses the PEP 8 Bullshit.
            jovo = pref + 'JoinVoiceChannel'
            if message.content.startswith(pref + 'kill') or message.content.startswith(pref + 'changelog'):
                return
            elif message.content.startswith(pref + 'raid') or message.content.startswith(pref + 'source'):
                return
            elif message.content.startswith(pref + 'prune') or message.content.startswith(pref + 'game'):
                return
            elif message.content.startswith(pref + 'remgame') or message.content.startswith(pref + 'join'):
                return
            elif message.content.startswith(pref + 'update') or message.content.startswith(pref + 'say'):
                return
            elif message.content.startswith(pref + 'type') or message.content.startswith(pref + 'uptime'):
                return
            elif message.content.startswith(pref + 'reload') or message.content.startswith(pref + 'pyversion'):
                return
            elif message.content.startswith(pref + 'Libs') or message.content.startswith(pref + 'userinfo'):
                return
            elif message.content.startswith(pref + 'kick') or message.content.startswith(pref + 'ban'):
                return
            elif message.content.startswith(pref + 'softban') or message.content.startswith(pref + 'clear'):
                return
            elif message.content.startswith(pref + 'ignorechannel') or message.content.startswith(pref + unig):
                return
            elif message.content.startswith(pref + 'tinyurl') or message.content.startswith(jovo):
                return
            elif message.content.startswith(pref + 'play') or message.content.startswith(pref + 'pause'):
                return
            elif message.content.startswith(pref + 'unpause') or message.content.startswith(pref + 'stop'):
                return
            elif message.content.startswith(pref + 'move') or message.content.startswith(pref + 'LeaveVoiceChannel'
                                                                                         ):
                return
            elif message.content.startswith(pref + 'Playlist'):
                return
            else:
                if message.channel.server.id == "140849390079180800":
                    return
                elif message.author.id == self.user.id:
                    return
                elif message.channel.server.id == "110373943822540800":
                    if message.author.id == "103607047383166976":
                        return
                    else:
                        info2 = str(self.botmessages['On_Bot_Mention_Message_Data'][0]).format(message.author)
                        yield from self.send_message(message.channel, content=info2)
                elif message.channel.server.id == '101596364479135744':
                    if message.author.id == "110368240768679936":
                        return
                    else:
                        info2 = str(self.botmessages['On_Bot_Mention_Message_Data'][0]).format(message.author)
                        yield from self.send_message(message.channel, content=info2)
                else:
                    info2 = str(self.botmessages['On_Bot_Mention_Message_Data'][0]).format(message.author)
                    try:
                        yield from self.send_message(message.channel, content=info2)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error_old(self, message)

    def login_helper(self):
        """
        Bot Login Helper.
        :return: Nothing.
        """
        while True:
            ret = self.login_info()
            if ret is not None and ret is not -1:
                break

    # Login stuff.

    @async
    def __ffs__(self, *args, **kwargs):
        yield from self.login(*args, **kwargs)
        yield from self.connect()

    def login_info(self):
        """
        Allows the bot to Connect / Reconnect.
        NOTE: Reconnection is not always 100% due to sometimes throwing a RuntimeError because of a Event loop getting
        closed in Discord.py. Sadly the run fucntion does not reopen/recreate that loop.
        :return: Nothing.
        """
        if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
            try:
                if self.discord_user_email and self.discord_user_password is not None:
                    self.is_bot_logged_in = True
                    self.loop.run_until_complete(self.__ffs__(self.discord_user_email, self.discord_user_password))
                elif self.bot_token is not None:
                    self.is_bot_logged_in = True
                    self.loop.run_until_complete(self.__ffs__(self.bot_token))
            except discord.errors.GatewayNotFound:
                print(str(self.consoletext['Login_Gateway_No_Find'][0]))
                return -2
            except discord.errors.LoginFailure as e:
                if str(e) == "Improper credentials have been passed.":
                    print(str(self.consoletext['Login_Failure'][0]))
                    return -2
                elif str(e) == "Improper token has been passed.":
                    print(str(self.consoletext['Invalid_Token'][0]))
                    sys.exit(2)
            except TypeError:
                pass
            except KeyboardInterrupt:
                pass
            except asyncio.futures.InvalidStateError:
                self.reconnects += 1
                if self.reconnects != 0:
                    print('Bot is currently reconnecting for {0} times.'.format(str(self.reconnects)))
                    return -1
            except aiohttp.errors.ClientResponseError:
                self.reconnects += 1
                if self.reconnects != 0:
                    print('Bot is currently reconnecting for {0} times.'.format(str(self.reconnects)))
                    return -1
            except aiohttp.errors.ClientOSError:
                self.reconnects += 1
                if self.reconnects != 0:
                    print('Bot is currently reconnecting for {0} times.'.format(str(self.reconnects)))
                    return -1
            if self.is_bot_logged_in:
                if not self.is_logged_in:
                    pass
                else:
                    self.reconnects += 1
                    if self.reconnects != 0:
                        print('Bot is currently reconnecting for {0} times.'.format(str(self.reconnects)))
                        return -1
        else:
            print(str(self.consoletext['Credentials_Not_Found'][0]))
            sys.exit(2)

    @async
    def on_login(self):
        """
        Function that does the on_ready event stuff after logging in.
        :return: Nothing.
        """
        if self.logged_in:
            self.logged_in = False
            message_data = str(self.botmessages['On_Ready_Message'][0])
            try:
                yield from self.send_message(discord.Object(id='118098998744580098'), content=message_data)
            except discord.errors.Forbidden:
                return
            try:
                yield from self.send_message(discord.Object(id='103685935593435136'), content=message_data)
            except discord.errors.Forbidden:
                return
            bot_name = self.user.name
            print(Fore.GREEN + Back.BLACK + Style.BRIGHT + str(
                self.consoletext['Window_Login_Text'][0]).format(bot_name, self.user.id, __version__))
            sys.stdout = open('{0}{1}resources{1}Logs{1}console.log'.format(self.path, self.sepa), 'w')
            sys.stderr = open('{0}{1}resources{1}Logs{1}unhandled_tracebacks.log'.format(self.path, self.sepa),
                              'w')
        if not self.logged_in:
            game_name = str(self.consoletext['On_Ready_Game'][0])
            stream_url = "https://twitch.tv/decoraterbot"
            yield from self.change_presence(game=discord.Game(name=game_name, type=1, url=stream_url))

    def variable(self):
        """
        Function that makes Certain things on the on_ready event only happen 1 time only. (eg the logged in printing
        stuff)
        :return: Nothing.
        """
        self.logged_in = True

    # Cache Cleanup.

    @async
    def verify_cache_cleanup_2(self, member):
        """
        Cleans Up Verify Cache.
        :param member: Member.
        :return: Nothing.
        """
        try:
            serveridslistfile = io.open('{0}{1}resources{1}ConfigData{1}serverconfigs{1}servers.json'.format(
                self.path, self.sepa))
            serveridslist = json.load(serveridslistfile)
            serveridslistfile.close()
            serverid = str(serveridslist['config_server_ids'][0])
            file_path = ('{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}verifications{0}'.format(self.sepa,
                                                                                                     serverid))
            filename_1 = 'verifycache.json'
            joinedlistfile = io.open(self.path + file_path + filename_1)
            newlyjoinedlist = json.load(joinedlistfile)
            joinedlistfile.close()
            if member.id in newlyjoinedlist['users_to_be_verified']:
                yield from self.send_message(discord.Object(id='141489876200718336'),
                                             content="{0} has left the {1} Server.".format(
                                                 member.mention, member.server.name))
                newlyjoinedlist['users_to_be_verified'].remove(member.id)
                file_name = "{0}verifications{0}verifycache.json".format(self.sepa)
                filename = "{0}{1}resources{1}ConfigData{1}serverconfigs{1}71324306319093760{2}".format(self.path,
                                                                                                        self.sepa,
                                                                                                        file_name)
                json.dump(newlyjoinedlist, open(filename, "w"))
        except Exception as e:
            funcname = 'verify_cache_cleanup_2'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @async
    def verify_cache_cleanup(self, member):
        """
        Cleans Up Verify Cache.
        :param member: Member.
        :return: Nothing.
        """
        try:
            serveridslistfile = io.open('{0}{1}resources{1}ConfigData{1}serverconfigs{1}servers.json'.format(
                self.path, self.sepa))
            serveridslist = json.load(serveridslistfile)
            serveridslistfile.close()
            serverid = str(serveridslist['config_server_ids'][0])
            file_path = '{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}verifications{0}'.format(self.sepa, serverid)
            filename_1 = 'verifycache.json'
            joinedlistfile = io.open(self.path + file_path + filename_1)
            newlyjoinedlist = json.load(joinedlistfile)
            joinedlistfile.close()
            if member.id in newlyjoinedlist['users_to_be_verified']:
                newlyjoinedlist['users_to_be_verified'].remove(member.id)
                file_name = "{0}verifications{0}verifycache.json".format(self.sepa)
                filename = "{0}{1}resources{1}ConfigData{1}serverconfigs{1}71324306319093760{2}".format(self.path,
                                                                                                        self.sepa,
                                                                                                        file_name)
                json.dump(newlyjoinedlist, open(filename, "w"))
        except Exception as e:
            funcname = 'verify_cache_cleanup'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)


def main():
    """
    EntryPoint to DecoraterBot.
    :return: Nothing.
    """
    BotClient(command_prefix=config.bot_prefix, description=config.description, pm_help=False)
