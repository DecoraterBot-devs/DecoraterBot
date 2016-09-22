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
import asyncio
import sys
import json
import io
import os.path
import importlib
import traceback
import ctypes
try:
    import BotCommands
except SyntaxError:
    sepa = os.sep
    exception_data = 'Fatal exception caused in BotCommands.py:\n{0}'.format(str(traceback.format_exc()))
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
    logfile = '{0}{1}resources{1}Logs{1}error_log.txt'.format(path, sepa)
    try:
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.seek(0)
            file.truncate()
        file.write(exception_data)
        file.close()
    except PermissionError:
        pass
    print('Cannot Continue as the Commands has a SyntaxError.')
    sys.exit(1)
try:
    import BotPMError
except ImportError:
    print('Some Unknown thing happened which made a critical bot code file unable to be found.')
import BotVoiceCommands
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

        try:
            self.consoledatafile = io.open('{0}{1}resources{1}ConfigData{1}ConsoleWindow.json'.format(
                self.path, self.sepa))
            self.consoletext = json.load(self.consoledatafile)
            self.consoledatafile.close()
        except FileNotFoundError:
            print('ConsoleWindow.json is not Found. Cannot Continue.')
            sys.exit(2)
        try:
            self.jsonfile = io.open('{0}{1}resources{1}ConfigData{1}IgnoreList.json'.format(self.path, self.sepa))
            self.somedict = json.load(self.jsonfile)
            self.jsonfile.close()
        except FileNotFoundError:
            print(str(self.consoletext['Missing_JSON_Errors'][0]))
            sys.exit(2)
        try:
            self.botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.json'.format(
                self.path, self.sepa))
            self.botmessages = json.load(self.botmessagesdata)
            self.botmessagesdata.close()
        except FileNotFoundError:
            print(str(self.consoletext['Missing_JSON_Errors'][1]))
            sys.exit(2)
        self.DBCommands = BotCommands.BotCommands()
        self.DBVoiceCommands = BotVoiceCommands.VoiceBotCommands()
        # default to True in case options are not present in Credentials.json
        self._logging = True
        self._logbans = True
        self._logunbans = True
        self._logkicks = True
        self._discord_logger = True
        self._asyncio_logger = True
        self._log_available = True
        self._log_unavailable = True
        self.log_channel_create = True
        self.log_channel_delete = True
        self.log_channel_update = True
        self.log_member_update = True
        self.log_server_join = True
        self.log_server_remove = True
        self.log_server_update = True
        self.log_server_role_create = True
        self.log_server_role_delete = True
        self.log_server_role_update = True
        self.log_group_join = True
        self.log_group_remove = True
        self.log_error = True
        self.log_voice_state_update = True
        self.log_typing = True
        self.log_socket_raw_receive = True
        self.log_socket_raw_send = True
        self.log_resumed = True
        self.log_member_join = True
        # Will Always be True to prevent the Error Handler from Causing Issues later.
        # Well only if the PM Error handler is False.
        self.enable_error_handler = True
        self.PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(self.path, self.sepa)
        if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
            self.BotConfig = BotConfigReader.BotConfigVars()
            discord_user_id = self.BotConfig.discord_user_id
            if discord_user_id == 'None':
                self.discord_user_id = None
            self._logging = self.BotConfig.logging
            self._logbans = self.BotConfig.logbans
            self._logunbans = self.BotConfig.logunbans
            self._logkicks = self.BotConfig.logkicks
            self._bot_prefix = self.BotConfig.bot_prefix
            if self._bot_prefix == '':
                self._bot_prefix = None
            if self._bot_prefix is None:
                print('No Prefix specified in Credentials.json. The Bot cannot continue.')
                sys.exit(2)
            self._disable_voice_commands = self.BotConfig.disable_voice_commands
            self._pm_command_errors = self.BotConfig.pm_command_errors
            self._discord_logger = self.BotConfig.discord_logger
            self._asyncio_logger = self.BotConfig.asyncio_logger
            self._log_available = self.BotConfig.log_available
            self._log_unavailable = self.BotConfig.log_unavailable
            self.log_channel_create = self.BotConfig.log_channel_create
            self.log_channel_delete = self.BotConfig.log_channel_delete
            self.log_channel_update = self.BotConfig.log_channel_update
            self.log_member_update = self.BotConfig.log_member_update
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
        if (self._logging or self._logbans or self._logunbans or self._logkicks or self._discord_logger or
                self._asyncio_logger or self._log_available or self._log_unavailable or self.log_channel_create or
                self.log_channel_delete or self.log_channel_update or self.log_member_update or self.log_server_join or
                self.log_server_remove or self.log_server_update or self.log_server_role_create or
                self.log_server_role_delete or self.log_server_role_update or self.log_group_join or
                self.log_group_remove or self.log_error or self.log_voice_state_update or self.log_typing or
                self.log_socket_raw_receive or self.log_socket_raw_send or self.log_resumed or self.log_member_join or
                self.enable_error_handler):
            import BotLogs
            self.DBLogs = BotLogs.BotLogs()
        self._somebool = False
        self.reload_normal_commands = False
        self.reload_voice_commands = False

    @asyncio.coroutine
    def ignore_channel_code(self, client, message):
        """
        Makes the bot Ignore or not Ignore channels.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        if message.content.startswith(self._bot_prefix + 'ignorechannel'):
            if message.channel.id not in self.somedict["channels"]:
                try:
                    self.somedict["channels"].append(message.channel.id)
                    json.dump(self.somedict, open("{0}{1}resources{1}ConfigData{1}IgnoreList.json".format(
                        self.path, self.sepa), "w"))
                    try:
                        yield from client.send_message(message.channel, str(self.botmessages['Ignore_Channel_Data'][0]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
                except Exception as e:
                    str(e)
                    try:
                        yield from client.send_message(message.channel, str(self.botmessages['Ignore_Channel_Data'][1]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(self._bot_prefix + 'unignorechannel'):
            if message.channel.id in self.somedict["channels"]:
                try:
                    ignored = self.somedict["channels"]
                    ignored.remove(message.channel.id)
                    json.dump(self.somedict, open("{0}{1}resources{1}ConfigData{1}IgnoreList.json".format(
                        self.path, self.sepa), "w"))
                    msg_info = str(self.botmessages['Unignore_Channel_Data'][0])
                    try:
                        yield from client.send_message(message.channel, msg_info)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
                except Exception as e:
                    str(e)
                    msg_info = str(self.botmessages['Unignore_Channel_Data'][1])
                    try:
                        yield from client.send_message(message.channel, msg_info)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def reload_command_code(self, client, message):
        """
        Reloads Bot Command Files.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        if message.content.startswith(self._bot_prefix + 'reload'):
            if message.author.id == self.discord_user_id:
                desmod_new = message.content.lower()[len(self._bot_prefix + 'reload '):].strip()
                rejoin_after_reload = False
                self._somebool = False
                desmod = None
                reload_reason = None
                if len(desmod_new) < 1:
                    desmod = None
                if desmod_new.rfind('botlogs') is not -1:
                    desmod = 'BotLogs'
                    rsn = desmod_new.replace('botlogs', "")
                    if rsn.rfind(' | ') is not -1:
                        reason = rsn.strip(' | ')
                        reload_reason = reason
                        self._somebool = True
                    else:
                        reason = None
                        reload_reason = reason
                        self._somebool = True
                elif desmod_new.rfind('botcommands') is not -1:
                    desmod = 'BotCommands'
                    rsn = desmod_new.replace('botcommands', "")
                    if rsn.rfind(' | ') is not -1:
                        reason = rsn.strip(' | ')
                        reload_reason = reason
                        self._somebool = True
                        self.reload_normal_commands = False
                    else:
                        reason = None
                        reload_reason = reason
                        self._somebool = True
                        self.reload_normal_commands = False
                elif desmod_new.rfind("botvoicecommands") is not -1:
                    desmod = "BotVoiceCommands"
                    rsn = desmod_new.replace('botvoicecommands', "")
                    if rsn.rfind(' | ') is not -1:
                        reason = rsn.replace(' | ', "")
                        reload_reason = reason
                        self._somebool = True
                        self.reload_voice_commands = False
                    else:
                        reason = None
                        reload_reason = reason
                        self._somebool = True
                        self.reload_voice_commands = False
                else:
                    self._somebool = False
                if self._somebool is True:
                    if desmod_new is not None:
                        if desmod == 'BotCommands' or desmod == 'BotLogs' or desmod == 'BotVoiceCommands':
                            if desmod == 'BotVoiceCommands':
                                rsn = reload_reason
                                rejoin_after_reload = True
                                yield from self.DBVoiceCommands.reload_commands_bypass1_new(client, message, rsn)
                            try:
                                module = sys.modules.get(desmod)
                                importlib.reload(module)
                                if self.reload_normal_commands:
                                    self.DBCommands = BotCommands.BotCommands()
                                if self.reload_voice_commands:
                                    self.DBVoiceCommands = BotVoiceCommands.VoiceBotCommands()
                                if rejoin_after_reload:
                                    yield from self.DBVoiceCommands.reload_commands_bypass2_new(
                                        client, message)
                                try:
                                    msgdata = str(self.botmessages['reload_command_data'][0])
                                    message_data = msgdata + ' Reloaded ' + desmod + '.'
                                    if desmod == 'BotLogs':
                                        if reload_reason is not None:
                                            message_data = message_data + ' Reason: ' + reload_reason
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
    def ignored_channel_commands_code(self, client, message):
        """
        Listens for the Commands that can be done in muted Channels.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.ignore_channel_code(client, message)
        yield from self.reload_command_code(client, message)

    @asyncio.coroutine
    def enable_all_commands_code(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.DBCommands.prune(client, message)
        yield from self.DBCommands.invite(client, message)
        yield from self.DBCommands.kills(client, message)
        yield from self.DBCommands.colors(client, message)
        yield from self.DBCommands.games(client, message)
        yield from self.DBCommands.attack(client, message)
        yield from self.DBCommands.debug(client, message)
        yield from self.DBCommands.other_commands(client, message)
        yield from self.DBCommands.userdata(client, message)
        yield from self.DBCommands.bot_say(client, message)
        yield from self.DBCommands.randomcoin(client, message)
        yield from self.DBCommands.mod_commands(client, message)
        yield from self.DBCommands.bot_roles(client, message)
        yield from self.DBCommands.more_commands(client, message)
        yield from self.DBCommands.convert_url(client, message)
        if self._disable_voice_commands is not True and sys.platform.startswith('win'):
            # Sorry but currently I only have opus for Windows and the same for ffmpeg.
            # You will have to get opus and ffmpeg for your platform and then add it to the list like you can see in
            # Core.py.
            yield from self.DBVoiceCommands.voice_stuff_new(client, message)
        else:
            yield from self.DBVoiceCommands.voice_stuff_new_disabled(client, message)
        yield from self.ignored_channel_commands_code(client, message)

    @asyncio.coroutine
    def enable_all_commands_with_send_logs_code(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.enable_all_commands_code(client, message)
        if self._logging:
            yield from self.DBLogs.send_logs(client, message)

    @asyncio.coroutine
    def enable_all_commands_with_logs_code(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.enable_all_commands_code(client, message)
        if self._logging:
            self.DBLogs.logs(message)

    @asyncio.coroutine
    def pm_commands_code(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.DBCommands.scan_for_invite_url_only_pm(client, message)
        yield from self.DBCommands.invite(client, message)
        yield from self.DBCommands.kills(client, message)
        yield from self.DBCommands.games(client, message)
        yield from self.DBCommands.other_commands(client, message)
        yield from self.DBCommands.bot_say(client, message)
        yield from self.DBCommands.randomcoin(client, message)
        yield from self.DBCommands.convert_url(client, message)
        if self._logging:
            self.DBLogs.logs(message)

    @asyncio.coroutine
    def cheesy_commands_code(self, client, message):
        """
        Listens fCheese.lab Specific Server commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.enable_all_commands_with_logs_code(client, message)
        serveridslistfile = io.open('{0}{1}resources{1}ConfigData{1}serverconfigs{1}servers.json'.format(self.path,
                                                                                                         self.sepa))
        serveridslist = json.load(serveridslistfile)
        serveridslistfile.close()
        serverid = str(serveridslist['config_server_ids'][0])
        file_path = ('{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}verifications{0}'.format(self.sepa, serverid))
        filename_1 = 'verifycache.json'
        filename_2 = 'verifycommand.json'
        filename_3 = 'verifyrole.json'
        filename_4 = 'verifymessages.json'
        filename_5 = 'verifycache.json'
        joinedlistfile = io.open(self.path + file_path + filename_1)
        newlyjoinedlist = json.load(joinedlistfile)
        joinedlistfile.close()
        memberjoinverifymessagefile = io.open(self.path + file_path + filename_2)
        memberjoinverifymessagedata = json.load(memberjoinverifymessagefile)
        memberjoinverifymessagefile.close()
        memberjoinverifyrolefile = io.open(self.path + file_path + filename_3)
        memberjoinverifyroledata = json.load(memberjoinverifyrolefile)
        memberjoinverifyrolefile.close()
        memberjoinverifymessagefile2 = io.open(self.path + file_path + filename_4)
        memberjoinverifymessagedata2 = json.load(memberjoinverifymessagefile2)
        memberjoinverifymessagefile2.close()
        role_name = str(memberjoinverifyroledata['verify_role_id'][0])
        msg_command = str(memberjoinverifymessagedata['verify_command'][0])
        try:
            msgdata = None
            if '>' or '<' or '`' in message.content:
                msgdata = message.content.replace('<', '').replace('>', '').replace('`', '')
            else:
                msgdata = message.content
            if msgdata == msg_command:
                if message.author.id in newlyjoinedlist['users_to_be_verified']:
                    yield from client.delete_message(message)
                    role2 = discord.utils.find(lambda role: role.id == role_name, message.channel.server.roles)
                    msg_data = str(memberjoinverifymessagedata2['verify_messages'][1]).format(message.server.name)
                    yield from client.add_roles(message.author, role2)
                    yield from client.send_message(message.author, msg_data)
                    newlyjoinedlist['users_to_be_verified'].remove(message.author.id)
                    json.dump(newlyjoinedlist, open(self.path + file_path + filename_5, "w"))
                else:
                    yield from client.delete_message(message)
                    yield from client.send_message(message.channel, str(
                        memberjoinverifymessagedata2['verify_messages'][2]))
            else:
                if message.author.id != client.user.id:
                    if message.author.id in newlyjoinedlist['users_to_be_verified']:
                        yield from client.delete_message(message)
                        yield from client.send_message(message.channel, str(
                            memberjoinverifymessagedata2['verify_messages'][3]).format(message.author.mention))
        except NameError:
            yield from client.send_message(message.channel, str(
                memberjoinverifymessagedata2['verify_messages'][4]).format(message.author.mention))

    @asyncio.coroutine
    def everyone_mention_logger_code(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        # if message.content.find('@everyone') != -1:
        #     yield from client.send_message(message.channel.server.owner,
        #                                    "{0} has mentioned everyone in {1} on the {1} server.".format(
        #                                        message.author.name, message.channel.name,
        #                                        message.channel.server.name))
        pass  # this does not yet work right so commented this out.

    @asyncio.coroutine
    def ignore_code(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        if message.channel.id not in self.somedict['channels']:
            try:
                if message.channel.is_private is not False:
                    yield from self.pm_commands_code(client, message)
                elif message.channel.server and message.channel.server.id == "81812480254291968":
                    if message.author.id == client.user.id:
                        return
                    elif message.channel.id == "153055192873566208":
                        yield from self.enable_all_commands_code(client, message)
                    elif message.channel.id == "87382611688689664":
                        yield from self.enable_all_commands_code(client, message)
                    else:
                        yield from self.enable_all_commands_with_send_logs_code(client, message)
                elif message.channel.server and message.channel.server.id == "71324306319093760":
                    if message.channel.id == '141489876200718336':
                        yield from self.cheesy_commands_code(client, message)
                    else:
                        yield from self.everyone_mention_logger_code(client, message)
                        yield from self.enable_all_commands_with_logs_code(client, message)
                else:
                    yield from self.enable_all_commands_with_logs_code(client, message)
            except Exception as e:
                if self._pm_command_errors:
                    if self.discord_user_id is not None:
                        owner = self.discord_user_id
                        exception_data2 = str(traceback.format_exc())
                        message_data = '```py\n{0}\n```'.format(exception_data2)
                        try:
                            yield from client.send_message(discord.User(id=owner), message_data)
                        except discord.errors.Forbidden:
                            return
                        except discord.errors.HTTPException:
                            funcname = 'ignore_code'
                            tbinfo = str(traceback.format_exc())
                            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)
                    else:
                        return
                else:
                    funcname = 'ignore_code'
                    tbinfo = str(traceback.format_exc())
                    yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)
        else:
            yield from self.ignored_channel_commands_code(client, message)

    @asyncio.coroutine
    def resolve_delete_method_code(self, client, message):
        """
        Handles Deleted Messages.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        try:
            if message.channel.is_private is not False:
                if self._logging:
                    self.DBLogs.delete_logs(message)
            elif message.channel.server and message.channel.server.id == "81812480254291968":
                if message.author.id == client.user.id:
                    return
                elif message.channel.id == "153055192873566208":
                    return
                elif message.channel.id == "87382611688689664":
                    return
                else:
                    yield from self.DBLogs.send_delete_logs(client, message)
            else:
                if message.channel.is_private is not False:
                    return
                elif message.channel.server.id == '95342850102796288':
                    return
                else:
                    if self._logging:
                        self.DBLogs.delete_logs(message)
        except Exception as e:
            funcname = '_resolve_delete_method_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def resolve_edit_method_code(self, client, before, after):
        """
        Handles Edited Messages.
        :param client: Discord client.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        try:
            if before.channel.is_private is not False:
                if self._logging:
                    self.DBLogs.edit_logs(before, after)
            elif before.channel.server and before.channel.server.id == "81812480254291968":
                if before.author.id == client.user.id:
                    return
                elif before.channel.id == "153055192873566208":
                    return
                elif before.channel.id == "87382611688689664":
                    return
                else:
                    yield from self.DBLogs.send_edit_logs(client, before, after)
            else:
                if before.channel.is_private is not False:
                    return
                elif before.channel.server.id == '95342850102796288':
                    return
                else:
                    if self._logging:
                        self.DBLogs.edit_logs(before, after)
        except Exception as e:
            funcname = '_resolve_edit_method_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def resolve_verify_cache_cleanup_2_code(self, client, member):
        """
        Cleans Up Verify Cache.
        :param client: Discord client.
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
                yield from client.send_message(discord.Object(id='141489876200718336'),
                                               "{0} has left the {1} Server.".format(
                                                   member.mention, member.server.name))
                newlyjoinedlist['users_to_be_verified'].remove(member.id)
                file_name = "{0}verifications{0}verifycache.json".format(self.sepa)
                filename = "{0}{1}resources{1}ConfigData{1}serverconfigs{1}71324306319093760{2}".format(self.path,
                                                                                                        self.sepa,
                                                                                                        file_name)
                json.dump(newlyjoinedlist, open(filename, "w"))
        except Exception as e:
            funcname = '_resolve_verify_cache_cleanup_2_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def resolve_verify_cache_cleanup_code(self, member):
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
            funcname = '_resolve_verify_cache_cleanup_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def resolve_onban_code(self, client, member):
        """
        Lists users banned.
        :param client: Discord client.
        :param member: Member.
        :return: Nothing.
        """
        str(client)  # to bypass unused param.
        try:
            if self._logbans:
                yield from self.DBLogs.onban(member)
            if member.server and member.server.id == "71324306319093760":
                yield from self.resolve_verify_cache_cleanup_code(member)
        except Exception as e:
            funcname = '_resolve_onban_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def resolve_onunban_code(self, server, user):
        """
        Lists users unbanned.
        :param server: Server.
        :param user: Member.
        :return: Nothing.
        """
        try:
            if self._logunbans:
                yield from self.DBLogs.onunban(server, user)
        except Exception as e:
            funcname = '_resolve_onunban_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def resolve_onremove_code(self, client, member):
        """
        Handles when a user is removed from a server.
        :param client: Discord client.
        :param member: Member.
        :return: Nothing.
        """
        try:
            try:
                banslist = yield from client.get_bans(member.server)
                if member in banslist:
                    return
                else:
                    if self._logkicks:
                        yield from self.DBLogs.onkick(member)
            except (discord.errors.HTTPException, discord.errors.Forbidden):
                if self._logkicks:
                    yield from self.DBLogs.onkick(member)
            if member.server and member.server.id == "71324306319093760":
                yield from self.resolve_verify_cache_cleanup_2_code(client, member)
        except Exception as e:
            funcname = '_resolve_onremove_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def resolve_onjoin_code(self, client, member):
        """
        Handles when a user joins a server.
        :param client: Discord client.
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
                yield from client.send_message(discord.Object(id=des_channel), message_data)
                if member.id in newlyjoinedlist['users_to_be_verified']:
                    # since this person is already in the list lets not readd them.
                    pass
                else:
                    newlyjoinedlist['users_to_be_verified'].append(member.id)
                    json.dump(newlyjoinedlist, open(self.path + file_path_join_2 + filename_join_4, "w"))
        except Exception as e:
            funcname = '_resolve_onjoin_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def resolve_on_login_voice_channel_join_code(self, client):
        """
        Joins a voice channel upon login (if one is set in the json file this reads.)
        :param client: Discord client.
        :return: Nothing.
        """
        try:
            if self._disable_voice_commands is not True:
                yield from self.DBVoiceCommands.reload_commands_bypass3_new(client)
            else:
                return
        except Exception as e:
            funcname = '_resolve_on_login_voice_channel_join_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def high_level_reload_helper_code(self, client, message, reload_reason):
        """
        Handles High level reloading.
        :param client: Discord client.
        :param message: Message.
        :param reload_reason: Reason for reloading.
        :return: Nothing.
        """
        try:
            if self._disable_voice_commands is not True:
                yield from self.DBVoiceCommands.reload_commands_bypass4_new(client, message, reload_reason)
            else:
                return
        except Exception as e:
            funcname = 'high_level_reload_helper_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    def resolve_discord_logger_code(self):
        """
        Discord Logger.
        :return: Nothing.
        """
        if self._discord_logger:
            self.DBLogs.set_up_discord_logger()

    def resolve_asyncio_logger_code(self):
        """
        asyncio Logger (seems to still not work yet for some reason).
        :return: Nothing.
        """
        if self._asyncio_logger:
            self.DBLogs.set_up_asyncio_logger()

    @asyncio.coroutine
    def server_available_code(self, server):
        """
        Gets Available servers.
        :param server: Server.
        :return: Nothing.
        """
        if self._log_available:
            yield from self.DBLogs.onavailable(server)

    @asyncio.coroutine
    def server_unavailable_code(self, server):
        """
        Gets Unavailable servers.
        :param server: Server.
        :return: Nothing.
        """
        if self._log_unavailable:
            yield from self.DBLogs.onunavailable(server)

    @asyncio.coroutine
    def resolve_ongroupjoin_code(self, channel, user):
        """
        Handles when a user joins a group.
        :param channel: Channel.
        :param user: User.
        :return: Nothing.
        """
        try:
            if self.log_group_join:
                yield from self.DBLogs.ongroupjoin(channel, user)
        except Exception as e:
            funcname = '_resolve_ongroupjoin_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def resolve_ongroupremove_code(self, channel, user):
        """
        Handles when a user is removed/leaves a group.
        :param channel: Channel.
        :param user: User.
        :return: Nothing.
        """
        try:
            if self.log_group_remove:
                yield from self.DBLogs.ongroupremove(channel, user)
        except Exception as e:
            funcname = '_resolve_ongroupremove_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)

    @asyncio.coroutine
    def high_level_reload_helper2_code(self, client, message):
        """
        Handles High level reloading.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        try:
            if self._disable_voice_commands is not True:
                yield from self.DBVoiceCommands.reload_commands_bypass2_new(client, message)
            else:
                return
        except Exception as e:
            funcname = 'high_level_reload_helper2_code'
            tbinfo = str(traceback.format_exc())
            yield from self.DBLogs.on_bot_error(funcname, tbinfo, e)


class BotIgnores:
    """
    Bot Ignores Class.
    """
    def __init__(self):
        self.bot = BotData()

    @asyncio.coroutine
    def ignore(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.ignore_code(client, message)

    @asyncio.coroutine
    def ignore_channel(self, client, message):
        """
        Makes the bot Ignore or not Ignore channels.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.ignore_channel_code(client, message)

    @asyncio.coroutine
    def reload_command(self, client, message):
        """
        Reloads Bot Command Files.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.reload_command_code(client, message)

    @asyncio.coroutine
    def ignored_channel_commands(self, client, message):
        """
        Listens for the Commands that can be done in muted Channels.
        :param client: Discord Client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.ignored_channel_commands_code(client, message)

    @asyncio.coroutine
    def enable_all_commands(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.enable_all_commands_code(client, message)

    @asyncio.coroutine
    def enable_all_commands_with_send_logs(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.enable_all_commands_with_send_logs_code(client, message)

    @asyncio.coroutine
    def enable_all_commands_with_logs(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.enable_all_commands_with_logs_code(client, message)

    @asyncio.coroutine
    def pm_commands(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.pm_commands_code(client, message)

    @asyncio.coroutine
    def cheesy_commands(self, client, message):
        """
        Listens fCheese.lab Specific Server commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.cheesy_commands_code(client, message)

    @asyncio.coroutine
    def everyone_mention_logger(self, client, message):
        """
        Listens for all Bot Commands.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.everyone_mention_logger_code(client, message)

    @asyncio.coroutine
    def resolve_delete_method(self, client, message):
        """
        Handles Deleted Messages.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.resolve_delete_method_code(client, message)

    @asyncio.coroutine
    def resolve_edit_method(self, client, before, after):
        """
        Handles Edited Messages.
        :param client: Discord client.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        yield from self.bot.resolve_edit_method_code(client, before, after)

    @asyncio.coroutine
    def resolve_onban(self, client, member):
        """
        Lists users banned.
        :param client: Discord client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.bot.resolve_onban_code(client, member)

    @asyncio.coroutine
    def resolve_onunban(self, server, user):
        """
        Lists users unbanned.
        :param server: Server.
        :param user: Member.
        :return: Nothing.
        """
        yield from self.bot.resolve_onunban_code(server, user)

    @asyncio.coroutine
    def resolve_onremove(self, client, member):
        """
        Handles when a user is removed from a server.
        :param client: Discord client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.bot.resolve_onremove_code(client, member)

    @asyncio.coroutine
    def resolve_onjoin(self, client, member):
        """
        Handles when a user joins a server.
        :param client: Discord client.
        :param member: Member.
        :return: Nothing.
        """
        yield from self.bot.resolve_onjoin_code(client, member)

    @asyncio.coroutine
    def resolve_on_login_voice_channel_join(self, client):
        """
        Joins a voice channel upon login (if one is set in the json file this reads.)
        :param client: Discord client.
        :return: Nothing.
        """
        yield from self.bot.resolve_on_login_voice_channel_join_code(client)

    @asyncio.coroutine
    def high_level_reload_helper(self, client, message, reload_reason):
        """
        Handles High level reloading.
        :param client: Discord client.
        :param message: Message.
        :param reload_reason: Reason for reloading.
        :return: Nothing.
        """
        yield from self.bot.high_level_reload_helper_code(client, message, reload_reason)

    def resolve_discord_logger(self):
        """
        Discord Logger.
        :return: Nothing.
        """
        self.bot.resolve_discord_logger_code()

    def resolve_asyncio_logger(self):
        """
        asyncio Logger (seems to still not work yet for some reason).
        :return: Nothing.
        """
        self.bot.resolve_asyncio_logger_code()

    @asyncio.coroutine
    def server_available(self, server):
        """
        Gets Available servers.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.bot.server_available_code(server)

    @asyncio.coroutine
    def server_unavailable(self, server):
        """
        Gets Unavailable servers.
        :param server: Server.
        :return: Nothing.
        """
        yield from self.bot.server_unavailable_code(server)

    @asyncio.coroutine
    def resolve_ongroupjoin(self, channel, user):
        """
        Handles when a user joins a group.
        :param channel: Channel.
        :param user: User.
        :return: Nothing.
        """
        yield from self.bot.resolve_ongroupjoin_code(channel, user)

    @asyncio.coroutine
    def resolve_ongroupremove(self, channel, user):
        """
        Handles when a user is removed/leaves a group.
        :param channel: Channel.
        :param user: User.
        :return: Nothing.
        """
        yield from self.bot.resolve_ongroupremove_code(channel, user)

    @asyncio.coroutine
    def high_level_reload_helper2(self, client, message):
        """
        Handles High level reloading.
        :param client: Discord client.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.bot.high_level_reload_helper2_code(client, message)
