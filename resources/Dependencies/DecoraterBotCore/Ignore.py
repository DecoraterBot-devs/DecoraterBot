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
try:
    import BotCommands
except SyntaxError:
    sepa = os.sep
    exception_data = 'Fatal exception caused in BotCommands.py:\n{0}'.format(str(traceback.format_exc()))
    logfile = '{0}{1}resources{1}Logs{1}error_log.txt'.format(sys.path[0], sepa)
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
import BotPMError
import BotVoiceCommands

sepa = os.sep

try:
    consoledatafile = io.open('{0}{1}resources{1}ConfigData{1}ConsoleWindow.json'.format(sys.path[0], sepa))
    consoletext = json.load(consoledatafile)
    consoledatafile.close()
except FileNotFoundError:
    print('ConsoleWindow.json is not Found. Cannot Continue.')
    sys.exit(2)
try:
    jsonfile = io.open('{0}{1}resources{1}ConfigData{1}IgnoreList.json'.format(sys.path[0], sepa))
    somedict = json.load(jsonfile)
    jsonfile.close()
except FileNotFoundError:
    print(str(consoletext['Missing_JSON_Errors'][0]))
    sys.exit(2)
try:
    botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.json'.format(sys.path[0], sepa))
    botmessages = json.load(botmessagesdata)
    botmessagesdata.close()
except FileNotFoundError:
    print(str(consoletext['Missing_JSON_Errors'][1]))
    sys.exit(2)

DBCommands = BotCommands.BotCommands()
DBVoiceCommands = BotVoiceCommands.VoiceBotCommands()

global _somebool
_somebool = False

# default to True in case options are not present in Credentials.json
_logging = True
_logbans = True
_logunbans = True
_logkicks = True
_discord_logger = True
_asyncio_logger = True
_log_available = True
_log_unavailable = True
log_channel_create = True
log_channel_delete = True
log_channel_update = True
log_member_update = True
log_server_join = True
log_server_remove = True
log_server_update = True
log_server_role_create = True
log_server_role_delete = True
log_server_role_update = True
log_group_join = True
log_group_remove = True
log_error = True
log_voice_state_update = True
log_typing = True
log_socket_raw_receive = True
log_socket_raw_send = True
log_resumed = True
log_member_join = True
# Will Always be True to prevent the Error Handler from Causing Issues later.
# Well only if the PM Error handler is False.
enable_error_handler = True

PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(sys.path[0], sepa)
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    credsfile = io.open(PATH)
    credentials = json.load(credsfile)
    credsfile.close()
    discord_user_id = str(credentials['ownerid'][0])
    bot_id = str(credentials['botid'][0])
    _logging = str(credentials['logging'][0])
    _logbans = str(credentials['logbans'][0])
    _logunbans = str(credentials['logunbans'][0])
    _logkicks = str(credentials['logkicks'][0])
    _bot_prefix = str(credentials['bot_prefix'][0])
    _disable_voice_commands = str(credentials['disable_voice'][0])
    _pm_command_errors = str(credentials['pm_command_errors'][0])
    _discord_logger = str(credentials['discord_py_logger'][0])
    _asyncio_logger = str(credentials['asyncio_logger'][0])
    _log_available = str(credentials['LogServerAvailable'][0])
    _log_unavailable = str(credentials['LogServerUnavailable'][0])
    log_channel_create = str(credentials['log_channel_create'][0])
    log_channel_delete = str(credentials['log_channel_delete'][0])
    log_channel_update = str(credentials['log_channel_update'][0])
    log_member_update = str(credentials['log_member_update'][0])
    log_server_join = str(credentials['log_server_join'][0])
    log_server_remove = str(credentials['log_server_remove'][0])
    log_server_update = str(credentials['log_server_update'][0])
    log_server_role_create = str(credentials['log_server_role_create'][0])
    log_server_role_delete = str(credentials['log_server_role_delete'][0])
    log_server_role_update = str(credentials['log_server_role_update'][0])
    log_group_join = str(credentials['log_group_join'][0])
    log_group_remove = str(credentials['log_group_remove'][0])
    log_error = str(credentials['log_error'][0])
    log_voice_state_update = str(credentials['log_voice_state_update'][0])
    log_typing = str(credentials['log_typing'][0])
    log_socket_raw_receive = str(credentials['log_socket_raw_receive'][0])
    log_socket_raw_send = str(credentials['log_socket_raw_send'][0])
    log_resumed = str(credentials['log_resumed'][0])
    log_member_join = str(credentials['log_member_join'][0])
    if _logging == 'True':
        _logging = True
    elif _logging == 'False':
        _logging = False
    if _logbans == 'True':
        _logbans = True
    elif _logbans == 'False':
        _logbans = False
    if _logunbans == 'True':
        _logunbans = True
    elif _logunbans == 'False':
        _logunbans = False
    if _logkicks == 'True':
        _logkicks = True
    elif _logkicks == 'False':
        _logkicks = False
    if _log_available == 'True':
        _log_available = True
    elif _log_available == 'False':
        _log_available = False
    if _log_unavailable == 'True':
        _log_unavailable = True
    elif _log_unavailable == 'False':
        _log_unavailable = False
    if log_channel_create == 'True':
        log_channel_create = True
    elif log_channel_create == 'False':
        log_channel_create = False
    if log_channel_delete == 'True':
        log_channel_delete = True
    elif log_channel_delete == 'False':
        log_channel_delete = False
    if log_channel_update == 'True':
        log_channel_update = True
    elif log_channel_update == 'False':
        log_channel_update = False
    if log_member_update == 'True':
        log_member_update = True
    elif log_member_update == 'False':
        log_member_update = False
    if log_server_join == 'True':
        log_server_join = True
    elif log_server_join == 'False':
        log_server_join = False
    if log_server_remove == 'True':
        log_server_remove = True
    elif log_server_remove == 'False':
        log_server_remove = False
    if log_server_update == 'True':
        log_server_update = True
    elif log_server_update == 'False':
        log_server_update = False
    if log_server_role_create == 'True':
        log_server_role_create = True
    elif log_server_role_create == 'False':
        log_server_role_create = False
    if log_server_role_delete == 'True':
        log_server_role_delete = True
    elif log_server_role_delete == 'False':
        log_server_role_delete = False
    if log_server_role_update == 'True':
        log_server_role_update = True
    elif log_server_role_update == 'False':
        log_server_role_update = False
    if log_group_join == 'True':
        log_group_join = True
    elif log_group_join == 'False':
        log_group_join = False
    if log_group_remove == 'True':
        log_group_remove = True
    elif log_group_remove == 'False':
        log_group_remove = False
    if log_error == 'True':
        log_error = True
    elif log_error == 'False':
        log_error = False
    if log_voice_state_update == 'True':
        log_voice_state_update = True
    elif log_voice_state_update == 'False':
        log_voice_state_update = False
    if log_typing == 'True':
        log_typing = True
    elif log_typing == 'False':
        log_typing = False
    if log_socket_raw_receive == 'True':
        log_socket_raw_receive = True
    elif log_socket_raw_receive == 'False':
        log_socket_raw_receive = False
    if log_socket_raw_send == 'True':
        log_socket_raw_send = True
    elif log_socket_raw_send == 'False':
        log_socket_raw_send = False
    if log_resumed == 'True':
        log_resumed = True
    elif log_resumed == 'False':
        log_resumed = False
    if log_member_join == 'True':
        log_member_join = True
    elif log_member_join == 'False':
        log_member_join = False
    if _discord_logger == 'True':
        _discord_logger = True
    elif _discord_logger == 'False':
        _discord_logger = False
    if _asyncio_logger == 'True':
        _asyncio_logger = True
    elif _asyncio_logger == 'False':
        _asyncio_logger = False
    if _disable_voice_commands == 'True':
        _disable_voice_commands = True
    elif _disable_voice_commands == 'False':
        _disable_voice_commands = False
    if _pm_command_errors == 'True':
        _pm_command_errors = True
        enable_error_handler = False
    elif _pm_command_errors == 'False':
        _pm_command_errors = False
        enable_error_handler = True
    if _bot_prefix == '':
        _bot_prefix = None
    if _bot_prefix is None:
        print('No Prefix specified in Credentials.json. The Bot cannot continue.')
        sys.exit(2)
    if bot_id == 'None':
        bot_id = None
    if discord_user_id == 'None':
        discord_user_id = None

if (_logging or _logbans or _logunbans or _logkicks or _discord_logger or _asyncio_logger or _log_available or
        _log_unavailable or log_channel_create or log_channel_delete or log_channel_update or 
        log_member_update or log_server_join or log_server_remove or log_server_update or 
        log_server_role_create or log_server_role_delete or log_server_role_update or log_group_join or 
        log_group_remove or log_error or log_voice_state_update or log_typing or log_socket_raw_receive or 
        log_socket_raw_send or log_resumed or log_member_join or enable_error_handler):
    import BotLogs
    DBLogs = BotLogs.BotLogs()


class bot_data_001:
    """
        This Class is for Internal Use only!!!
    """

    def __init__(self):
        pass

    @asyncio.coroutine
    def ignore_channel_code(self, client, message):
        if message.content.startswith(_bot_prefix + 'ignorechannel'):
            if message.channel.id not in somedict["channels"]:
                try:
                    somedict["channels"].append(message.channel.id)
                    json.dump(somedict, open("{0}{1}resources{1}ConfigData{1}IgnoreList.json".format(sys.path[0],
                                                                                                     sepa), "w"))
                    try:
                        yield from client.send_message(message.channel, str(botmessages['Ignore_Channel_Data'][0]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
                except Exception as e:
                    try:
                        yield from client.send_message(message.channel, str(botmessages['Ignore_Channel_Data'][1]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'unignorechannel'):
            if message.channel.id in somedict["channels"]:
                try:
                    ignored = somedict["channels"]
                    ignored.remove(message.channel.id)
                    json.dump(somedict, open("{0}{1}resources{1}ConfigData{1}IgnoreList.json".format(sys.path[0],
                                                                                                     sepa), "w"))
                    msg_info = str(botmessages['Unignore_Channel_Data'][0])
                    try:
                        yield from client.send_message(message.channel, msg_info)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
                except Exception as e:
                    msg_info = str(botmessages['Unignore_Channel_Data'][1])
                    try:
                        yield from client.send_message(message.channel, msg_info)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def reload_command_code(self, client, message):
        global _somebool
        if message.content.startswith(_bot_prefix + 'reload'):
            if message.author.id == discord_user_id:
                desmod_new = message.content.lower()[len(_bot_prefix + 'reload '):].strip()
                rejoin_after_reload = False
                _somebool = False
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
                        _somebool = True
                    else:
                        reason = None
                        reload_reason = reason
                        _somebool = True
                elif desmod_new.rfind('botcommands') is not -1:
                    desmod = 'BotCommands'
                    rsn = desmod_new.replace('botcommands', "")
                    if rsn.rfind(' | ') is not -1:
                        reason = rsn.strip(' | ')
                        reload_reason = reason
                        _somebool = True
                    else:
                        reason = None
                        reload_reason = reason
                        _somebool = True
                elif desmod_new.rfind("botvoicecommands") is not -1:
                    desmod = "BotVoiceCommands"
                    rsn = desmod_new.replace('botvoicecommands', "")
                    if rsn.rfind(' | ') is not -1:
                        reason = rsn.replace(' | ', "")
                        reload_reason = reason
                        _somebool = True
                    else:
                        reason = None
                        reload_reason = reason
                        _somebool = True
                else:
                    _somebool = False
                if _somebool is True:
                    if desmod_new is not None:
                        if desmod == 'BotCommands' or desmod == 'BotLogs' or desmod == 'BotVoiceCommands':
                            if desmod == 'BotVoiceCommands':
                                rsn = reload_reason
                                rejoin_after_reload = True
                                yield from DBVoiceCommands.reload_commands_bypass1_new(client, message, rsn)
                            try:
                                module = sys.modules.get(desmod)
                                importlib.reload(module)
                                if rejoin_after_reload:
                                    yield from DBVoiceCommands.reload_commands_bypass2_new(
                                        client, message)
                                try:
                                    msgdata = str(botmessages['reload_command_data'][0])
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
        yield from DBCommands.prune(client, message)
        yield from DBCommands.invite(client, message)
        yield from DBCommands.kills(client, message)
        yield from DBCommands.colors(client, message)
        yield from DBCommands.games(client, message)
        yield from DBCommands.attack(client, message)
        yield from DBCommands.debug(client, message)
        yield from DBCommands.other_commands(client, message)
        yield from DBCommands.userdata(client, message)
        yield from DBCommands.bot_say(client, message)
        yield from DBCommands.randomcoin(client, message)
        yield from DBCommands.mod_commands(client, message)
        yield from DBCommands.bot_roles(client, message)
        yield from DBCommands.more_commands(client, message)
        yield from DBCommands.convert_url(client, message)
        if _disable_voice_commands is not True and sys.platform.startswith('win'):
            # Sorry but currently I only have opus for Windows and the same for ffmpeg.
            # You will have to get opus and ffmpeg for your platform and then add it to the list like you can see in
            # Core.py.
            yield from DBVoiceCommands.voice_stuff_new(client, message)
        else:
            yield from DBVoiceCommands.voice_stuff_new_disabled(client, message)
        yield from self.ignored_channel_commands_code(client, message)

    @asyncio.coroutine
    def enable_all_commands_with_send_logs_code(self, client, message):
        yield from self.enable_all_commands_code(client, message)
        if _logging:
            yield from DBLogs.send_logs(client, message)

    @asyncio.coroutine
    def enable_all_commands_with_logs_code(self, client, message):
        yield from self.enable_all_commands_code(client, message)
        if _logging:
            DBLogs.logs(client, message)

    @asyncio.coroutine
    def pm_commands_code(self, client, message):
        yield from DBCommands.scan_for_invite_url_only_pm(client, message)
        yield from DBCommands.invite(client, message)
        yield from DBCommands.kills(client, message)
        yield from DBCommands.games(client, message)
        yield from DBCommands.other_commands(client, message)
        yield from DBCommands.bot_say(client, message)
        yield from DBCommands.randomcoin(client, message)
        yield from DBCommands.convert_url(client, message)
        if _logging:
            DBLogs.logs(client, message)

    @asyncio.coroutine
    def cheesy_commands_code(self, client, message):
        yield from self.enable_all_commands_with_logs_code(client, message)
        serveridslistfile = io.open('{0}{1}resources{1}ConfigData{1}serverconfigs{1}servers.json'.format(sys.path[0],
                                                                                                         sepa))
        serveridslist = json.load(serveridslistfile)
        serveridslistfile.close()
        serverid = str(serveridslist['config_server_ids'][0])
        file_path = ('{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}verifications{0}'.format(sepa, serverid))
        filename_1 = 'verifycache.json'
        filename_2 = 'verifycommand.json'
        filename_3 = 'verifyrole.json'
        filename_4 = 'verifymessages.json'
        filename_5 = 'verifycache.json'
        joinedlistfile = io.open(sys.path[0] + file_path + filename_1)
        newlyjoinedlist = json.load(joinedlistfile)
        joinedlistfile.close()
        memberjoinverifymessagefile = io.open(sys.path[0] + file_path + filename_2)
        memberjoinverifymessagedata = json.load(memberjoinverifymessagefile)
        memberjoinverifymessagefile.close()
        memberjoinverifyrolefile = io.open(sys.path[0] + file_path + filename_3)
        memberjoinverifyroledata = json.load(memberjoinverifyrolefile)
        memberjoinverifyrolefile.close()
        memberjoinverifymessagefile2 = io.open(sys.path[0] + file_path + filename_4)
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
                    role = discord.utils.find(lambda role: role.id == role_name, message.channel.server.roles)
                    msg_data = str(memberjoinverifymessagedata2['verify_messages'][1]).format(message.server.name)
                    yield from client.add_roles(message.author, role)
                    yield from client.send_message(message.author, msg_data)
                    newlyjoinedlist['users_to_be_verified'].remove(message.author.id)
                    json.dump(newlyjoinedlist, open(sys.path[0] + file_path + filename_5, "w"))
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
        # if message.content.find('@everyone') != -1:
        #     yield from client.send_message(message.channel.server.owner,
        #                                    "{0} has mentioned everyone in {1} on the {1} server.".format(
        #                                        message.author.name, message.channel.name,
        #                                        message.channel.server.name))
        pass  # this does not yet work right so commented this out.


class bot_data_002:
    """
        This Class is for Internal Use only!!!
    """
    def __init__(self):
        self.DBCommandData = BotCommandData()

    @asyncio.coroutine
    def ignore_code(self, client, message):
        if message.channel.id not in somedict['channels']:
            try:
                if message.channel.is_private is not False:
                    yield from self.DBCommandData.pm_commands(client, message)
                elif message.channel.server and message.channel.server.id == "81812480254291968":
                    if message.author.id == bot_id:
                        return
                    elif message.channel.id == "153055192873566208":
                        yield from self.DBCommandData.enable_all_commands(client, message)
                    elif message.channel.id == "87382611688689664":
                        yield from self.DBCommandData.enable_all_commands(client, message)
                    else:
                        yield from self.DBCommandData.enable_all_commands_with_send_logs(client, message)
                elif message.channel.server and message.channel.server.id == "71324306319093760":
                    if message.channel.id == '141489876200718336':
                        yield from self.DBCommandData.cheesy_commands(client, message)
                    else:
                        yield from self.DBCommandData.everyone_mention_logger(client, message)
                        yield from self.DBCommandData.enable_all_commands_with_logs(client, message)
                else:
                    yield from self.DBCommandData.enable_all_commands_with_logs(client, message)
            except Exception as e:
                if _pm_command_errors:
                    if discord_user_id is not None:
                        owner = discord_user_id
                        exception_data = str(traceback.format_exc())
                        message_data = '```py\n' + exception_data + "\n```"
                        try:
                            yield from client.send_message(discord.User(id=owner), message_data)
                        except discord.errors.Forbidden:
                            return
                        except discord.errors.HTTPException:
                            funcname = 'ignore_code'
                            tbinfo = str(traceback.format_exc())
                            yield from DBLogs.on_bot_error(funcname, tbinfo)
                    else:
                        return
                else:
                    funcname = 'ignore_code'
                    tbinfo = str(traceback.format_exc())
                    yield from DBLogs.on_bot_error(funcname, tbinfo)
        else:
            yield from self.DBCommandData.ignored_channel_commands(client, message)


class bot_data_003:
    """
        This Class is for Internal Use only!!!
    """
    def __init__(self):
        pass

    @asyncio.coroutine
    def resolve_delete_method_code(self, client, message):
        try:
            if message.channel.is_private is not False:
                if _logging == 'True':
                    DBLogs.delete_logs(client, message)
            elif message.channel.server and message.channel.server.id == "81812480254291968":
                if message.author.id == bot_id:
                    return
                elif message.channel.id == "153055192873566208":
                    return
                elif message.channel.id == "87382611688689664":
                    return
                else:
                    yield from DBLogs.send_delete_logs(client, message)
            else:
                if message.channel.is_private is not False:
                    return
                elif message.channel.server.id == '95342850102796288':
                    return
                else:
                    if _logging == 'True':
                        DBLogs.delete_logs(client, message)
        except Exception as e:
            funcname = '_resolve_delete_method_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def resolve_edit_method_code(self, client, before, after):
        try:
            if before.channel.is_private is not False:
                if _logging == 'True':
                    DBLogs.edit_logs(client, before, after)
            elif before.channel.server and before.channel.server.id == "81812480254291968":
                if before.author.id == bot_id:
                    return
                elif before.channel.id == "153055192873566208":
                    return
                elif before.channel.id == "87382611688689664":
                    return
                else:
                    yield from DBLogs.send_edit_logs(client, before, after)
            else:
                if before.channel.is_private is not False:
                    return
                elif before.channel.server.id == '95342850102796288':
                    return
                else:
                    if _logging == 'True':
                        DBLogs.edit_logs(client, before, after)
        except Exception as e:
            funcname = '_resolve_edit_method_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def resolve_verify_cache_cleanup_2_code(self, client, member):
        try:
            serveridslistfile = io.open('{0}{1}resources{1}ConfigData{1}serverconfigs{1}servers.json'.format(
                sys.path[0], sepa))
            serveridslist = json.load(serveridslistfile)
            serveridslistfile.close()
            serverid = str(serveridslist['config_server_ids'][0])
            file_path = ('{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}verifications{0}'.format(sepa, serverid))
            filename_1 = 'verifycache.json'
            joinedlistfile = io.open(sys.path[0] + file_path + filename_1)
            newlyjoinedlist = json.load(joinedlistfile)
            joinedlistfile.close()
            if member.id in newlyjoinedlist['users_to_be_verified']:
                yield from client.send_message(discord.Object(id='141489876200718336'),
                                               "{0} has left the {1} Server.".format(
                                                   member.mention, member.server.name))
                newlyjoinedlist['users_to_be_verified'].remove(member.id)
                file_name = "{0}verifications{0}verifycache.json".format(sepa)
                filename = "{0}{1}resources{1}ConfigData{1}serverconfigs{1}71324306319093760{2}".format(sys.path[0],
                                                                                                        sepa, file_name)
                json.dump(newlyjoinedlist, open(filename, "w"))
        except Exception as e:
            funcname = '_resolve_verify_cache_cleanup_2_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def resolve_verify_cache_cleanup_code(self, client, member):
        try:
            serveridslistfile = io.open('{0}{1}resources{1}ConfigData{1}serverconfigs{1}servers.json'.format(
                sys.path[0], sepa))
            serveridslist = json.load(serveridslistfile)
            serveridslistfile.close()
            serverid = str(serveridslist['config_server_ids'][0])
            file_path = '{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}verifications{0}'.format(sepa, serverid)
            filename_1 = 'verifycache.json'
            joinedlistfile = io.open(sys.path[0] + file_path + filename_1)
            newlyjoinedlist = json.load(joinedlistfile)
            joinedlistfile.close()
            if member.id in newlyjoinedlist['users_to_be_verified']:
                newlyjoinedlist['users_to_be_verified'].remove(member.id)
                file_name = "{0}verifications{0}verifycache.json".format(sepa)
                filename = "{0}{1}resources{1}ConfigData{1}serverconfigs{1}71324306319093760{2}".format(sys.path[0],
                                                                                                        sepa, file_name)
                json.dump(newlyjoinedlist, open(filename, "w"))
        except Exception as e:
            funcname = '_resolve_verify_cache_cleanup_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def resolve_onban_code(self, client, member):
        try:
            if _logbans == 'True':
                yield from DBLogs.onban(client, member)
            if member.server and member.server.id == "71324306319093760":
                yield from self.resolve_verify_cache_cleanup_code(client, member)
        except Exception as e:
            funcname = '_resolve_onban_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def resolve_onunban_code(self, client, user):
        try:
            if _logunbans == 'True':
                yield from DBLogs.onunban(client, user)
        except Exception as e:
            funcname = '_resolve_onunban_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def resolve_onremove_code(self, client, member):
        try:
            try:
                banslist = yield from client.get_bans(member.server)
                if member in banslist:
                    return
                else:
                    if _logkicks == 'True':
                        yield from DBLogs.onkick(client, member)
            except (discord.errors.HTTPException, discord.errors.Forbidden):
                if _logkicks == 'True':
                    yield from DBLogs.onkick(client, member)
            if member.server and member.server.id == "71324306319093760":
                yield from self.resolve_verify_cache_cleanup_2_code(client, member)
        except Exception as e:
            funcname = '_resolve_onremove_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def resolve_onjoin_code(self, client, member):
        try:
            # TODO: Add logging for this.
            if member.server.id == '71324306319093760' and member.bot is not True:
                file_path_join_1 = '{0}resources{0}ConfigData{0}serverconfigs{0}'.format(sepa)
                filename_join_1 = 'servers.json'
                serveridslistfile = io.open(sys.path[0] + file_path_join_1 + filename_join_1)
                serveridslist = json.load(serveridslistfile)
                serveridslistfile.close()
                serverid = str(serveridslist['config_server_ids'][0])
                file_path_join_2 = '{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}verifications{0}'.format(sepa,
                                                                                                               serverid)
                filename_join_2 = 'verifymessages.json'
                filename_join_3 = 'verifycache.json'
                filename_join_4 = 'verifycache.json'
                memberjoinmessagedatafile = io.open(sys.path[0] + file_path_join_2 + filename_join_2)
                memberjoinmessagedata = json.load(memberjoinmessagedatafile)
                memberjoinmessagedatafile.close()
                msg_info = str(memberjoinmessagedata['verify_messages'][0])
                message_data = msg_info.format(member.id, member.server.name)
                des_channel = str(memberjoinmessagedata['verify_messages_channel'][0])
                joinedlistfile = io.open(sys.path[0] + file_path_join_2 + filename_join_3)
                newlyjoinedlist = json.load(joinedlistfile)
                joinedlistfile.close()
                yield from client.send_message(discord.Object(id=des_channel), message_data)
                if member.id in newlyjoinedlist['users_to_be_verified']:
                    # since this person is already in the list lets not readd them.
                    pass
                else:
                    newlyjoinedlist['users_to_be_verified'].append(member.id)
                    json.dump(newlyjoinedlist, open(sys.path[0] + file_path_join_2 + filename_join_4, "w"))
        except Exception as e:
            funcname = '_resolve_onjoin_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def resolve_on_login_voice_channel_join_code(self, client):
        try:
            if _disable_voice_commands is not True:
                yield from DBVoiceCommands.reload_commands_bypass3_new(client)
            else:
                return
        except Exception as e:
            funcname = '_resolve_on_login_voice_channel_join_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def high_level_reload_helper_code(self, client, message, reload_reason):
        try:
            if _disable_voice_commands is not True:
                yield from DBVoiceCommands.reload_commands_bypass4_new(client, message, reload_reason)
            else:
                return
        except Exception as e:
            funcname = 'high_level_reload_helper_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @staticmethod
    def resolve_discord_logger_code():
        if _discord_logger:
            DBLogs.set_up_discord_logger()

    @staticmethod
    def resolve_asyncio_logger_code():
        if _asyncio_logger:
            DBLogs.set_up_asyncio_logger()

    @asyncio.coroutine
    def server_available_code(self, server):
        if _log_available:
            yield from DBLogs.onavailable(server)

    @asyncio.coroutine
    def server_unavailable_code(self, server):
        if _log_unavailable:
            yield from DBLogs.onunavailable(server)

    @asyncio.coroutine
    def resolve_ongroupjoin_code(self, channel, user):
        try:
            if log_group_join:
                yield from DBLogs.ongroupjoin(channel, user)
        except Exception as e:
            funcname = '_resolve_ongroupjoin_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def resolve_ongroupremove_code(self, channel, user):
        try:
            if log_group_remove:
                yield from DBLogs.ongroupremove(channel, user)
        except Exception as e:
            funcname = '_resolve_ongroupremove_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)

    @asyncio.coroutine
    def high_level_reload_helper2_code(self, client, message):
        try:
            if _disable_voice_commands is not True:
                yield from DBVoiceCommands.reload_commands_bypass2_new(client, message)
            else:
                return
        except Exception as e:
            funcname = 'high_level_reload_helper2_code'
            tbinfo = str(traceback.format_exc())
            yield from DBLogs.on_bot_error(funcname, tbinfo)


class BotCommandData:
    def __init__(self):
        self.bot = bot_data_001()

    @asyncio.coroutine
    def ignore_channel(self, client, message):
        yield from self.bot.ignore_channel_code(client, message)

    @asyncio.coroutine
    def reload_command(self, client, message):
        yield from self.bot.reload_command_code(client, message)

    @asyncio.coroutine
    def ignored_channel_commands(self, client, message):
        yield from self.bot.ignored_channel_commands_code(client, message)

    @asyncio.coroutine
    def enable_all_commands(self, client, message):
        yield from self.bot.enable_all_commands_code(client, message)

    @asyncio.coroutine
    def enable_all_commands_with_send_logs(self, client, message):
        yield from self.bot.enable_all_commands_with_send_logs_code(client, message)

    @asyncio.coroutine
    def enable_all_commands_with_logs(self, client, message):
        yield from self.bot.enable_all_commands_with_logs_code(client, message)

    @asyncio.coroutine
    def pm_commands(self, client, message):
        yield from self.bot.pm_commands_code(client, message)

    @asyncio.coroutine
    def cheesy_commands(self, client, message):
        yield from self.bot.cheesy_commands_code(client, message)

    @asyncio.coroutine
    def everyone_mention_logger(self, client, message):
        yield from self.bot.everyone_mention_logger_code(client, message)


class BotIgnores:
    def __init__(self):
        self.bot = bot_data_002()

    @asyncio.coroutine
    def ignore(self, client, message):
        yield from self.bot.ignore_code(client, message)


class BotEvents:
    def __init__(self):
        self.bot = bot_data_003()

    @asyncio.coroutine
    def resolve_delete_method(self, client, message):
        yield from self.bot.resolve_delete_method_code(client, message)

    @asyncio.coroutine
    def resolve_edit_method(self, client, before, after):
        yield from self.bot.resolve_edit_method_code(client, before, after)

    @asyncio.coroutine
    def resolve_onban(self, client, member):
        yield from self.bot.resolve_onban_code(client, member)

    @asyncio.coroutine
    def resolve_onunban(self, client, user):
        yield from self.bot.resolve_onunban_code(client, user)

    @asyncio.coroutine
    def resolve_onremove(self, client, member):
        yield from self.bot.resolve_onremove_code(client, member)

    @asyncio.coroutine
    def resolve_onjoin(self, client, member):
        yield from self.bot.resolve_onjoin_code(client, member)

    @asyncio.coroutine
    def resolve_on_login_voice_channel_join(self, client):
        yield from self.bot.resolve_on_login_voice_channel_join_code(client)

    @asyncio.coroutine
    def high_level_reload_helper(self, client, message, reload_reason):
        yield from self.bot.high_level_reload_helper_code(client, message, reload_reason)

    def resolve_discord_logger(self):
        self.bot.resolve_discord_logger_code()

    def resolve_asyncio_logger(self):
        self.bot.resolve_asyncio_logger_code()

    @asyncio.coroutine
    def server_available(self, server):
        yield from self.bot.server_available_code(server)

    @asyncio.coroutine
    def server_unavailable(self, server):
        yield from self.bot.server_unavailable_code(server)

    @asyncio.coroutine
    def resolve_ongroupjoin(self, channel, user):
        yield from self.bot.resolve_ongroupjoin_code(channel, user)

    @asyncio.coroutine
    def resolve_ongroupremove(self, channel, user):
        yield from self.bot.resolve_ongroupremove_code(channel, user)

    @asyncio.coroutine
    def high_level_reload_helper2(self, client, message):
        yield from self.bot.high_level_reload_helper2_code(client, message)
