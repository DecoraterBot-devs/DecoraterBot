# coding=utf-8
import discord
import asyncio
import sys
import json
import io
import os.path
import importlib
import traceback
import BotCommands
import BotPMError
import BotVoiceCommands
from discord.ext import commands

global _somebool
global newlyjoinedlist
# noinspection PyRedeclaration
newlyjoinedlist = []
# noinspection PyRedeclaration
_somebool = False

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

# noinspection PyUnboundLocalVariable
if _logging == 'True' or _logbans == 'True' or _logunbans == 'True' or _logkicks == 'True':
    import BotLogs
try:
    consoledatafile = io.open(sys.path[0] + '\\resources\\ConfigData\\ConsoleWindow.json', 'r')
    consoletext = json.load(consoledatafile)
except FileNotFoundError:
    print('ConsoleWindow.json is not Found. Cannot Continue.')
    sys.exit(2)
try:
    jsonfile = io.open(sys.path[0] + '\\resources\\ConfigData\\IgnoreList.json', 'r')
    somedict = json.load(jsonfile)
except FileNotFoundError:
    print(str(consoletext['Missing_JSON_Errors'][0]))
    sys.exit(2)
try:
    botmessagesdata = io.open(sys.path[0] + '\\resources\\ConfigData\\BotMessages.json', 'r')
    botmessages = json.load(botmessagesdata)
except FileNotFoundError:
    print(str(consoletext['Missing_JSON_Errors'][1]))
    sys.exit(2)


class BotCommandData:
    def __init__(self, client):
        self.bot = client

    @classmethod
    async def _ignore_channel(self, client, message):
        if message.content.startswith(_bot_prefix + 'ignorechannel'):
            if message.channel.id not in somedict["channels"]:
                # noinspection PyUnusedLocal
                try:
                    somedict["channels"].append(message.channel.id)
                    json.dump(somedict, open(sys.path[0] + "\\resources\\ConfigData\\IgnoreList.json", "w"))
                    try:
                        await client.send_message(message.channel, str(botmessages['Ignore_Channel_Data'][0]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
                except Exception as e:
                    try:
                        await client.send_message(message.channel, str(botmessages['Ignore_Channel_Data'][1]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'unignorechannel'):
            if message.channel.id in somedict["channels"]:
                # noinspection PyUnusedLocal
                try:
                    ignored = somedict["channels"]
                    ignored.remove(message.channel.id)
                    json.dump(somedict, open(sys.path[0] + "\\resources\\ConfigData\\IgnoreList.json", "w"))
                    try:
                        await client.send_message(message.channel, str(botmessages['Unignore_Channel_Data'][0]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
                except Exception as e:
                    try:
                        await client.send_message(message.channel, str(botmessages['Unignore_Channel_Data'][1]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)

    # noinspection PyUnusedLocal
    @classmethod
    async def _reload_command(self, client, message):
        global _somebool
        if message.content.startswith(_bot_prefix + 'reload'):
            if message.author.id == discord_user_id:
                desmod_new = message.content.lower()[len(_bot_prefix + 'reload '):].strip()
                rejoin_after_reload = False
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
                        # noinspection PyUnboundLocalVariable
                        if desmod == 'BotCommands' or desmod == 'BotLogs' or desmod == 'BotVoiceCommands':
                            if desmod == 'BotVoiceCommands':
                                # to prevent leaving voice Channel when the commands are not reloaded.
                                # noinspection PyUnboundLocalVariable
                                rsn = reload_reason
                                # removed from BotCommands and moved to BotVoiceCommands.
                                # await BotCommands.BotCommands._reload_commands_bypass1(client, message, rsn)
                                # newly added.
                                rejoin_after_reload = True
                                await BotVoiceCommands.VoiceBotCommands._reload_commands_bypass1_new(client, message,
                                                                                                     rsn)
                            try:
                                module = sys.modules.get(desmod)
                                importlib.reload(module)
                                if rejoin_after_reload:
                                    # removed from BotCommands and moved to BotVoiceCommands.
                                    # await BotCommands.BotCommands._reload_commands_bypass2(client, message)
                                    # newly added.
                                    await BotVoiceCommands.VoiceBotCommands._reload_commands_bypass2_new(client,
                                                                                                         message)
                                try:
                                    msgdata = str(botmessages['reload_command_data'][0])
                                    message_data = msgdata + ' Reloaded ' + desmod + '.'
                                    if desmod == 'BotLogs':
                                        if reload_reason is not None:
                                            message_data = message_data + ' Reason: ' + reload_reason
                                            await client.send_message(message.channel, message_data)
                                        else:
                                            await client.send_message(message.channel, message_data)
                                    else:
                                        await client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                            except Exception as e:
                                reloadexception = str(traceback.format_exc())
                                try:
                                    reload_data = str(botmessages['reload_command_data'][1]) + '\n```py\n'
                                    await client.send_message(message.channel, reload_data + reloadexception + '```')
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                else:
                    try:
                        await client.send_message(message.channel, str(botmessages['reload_command_data'][2]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
            else:
                try:
                    await client.send_message(message.channel, str(botmessages['reload_command_data'][3]))
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)

    @classmethod
    async def ignored_channel_commands(self, client, message):
        await self._ignore_channel(client, message)
        await self._reload_command(client, message)

    @classmethod
    async def enable_all_commands(self, client, message):
        await BotCommands.BotCommands.prune(client, message)
        await BotCommands.BotCommands.invite(client, message)
        await BotCommands.BotCommands.kills(client, message)
        await BotCommands.BotCommands.colors(client, message)
        await BotCommands.BotCommands.games(client, message)
        await BotCommands.BotCommands.attack(client, message)
        await BotCommands.BotCommands.debug(client, message)
        await BotCommands.BotCommands.other_commands(client, message)
        await BotCommands.BotCommands.userdata(client, message)
        await BotCommands.BotCommands.bot_say(client, message)
        await BotCommands.BotCommands.randomcoin(client, message)
        await BotCommands.BotCommands.mod_commands(client, message)
        await BotCommands.BotCommands.bot_roles(client, message)
        await BotCommands.BotCommands.more_commands(client, message)
        await BotCommands.BotCommands.convert_url(client, message)
        # removed from BotCommands and moved to BotVoiceCommands.
        # await BotCommands.BotCommands.voice_stuff(client, message)
        await BotVoiceCommands.VoiceBotCommands.voice_stuff_new(client, message)
        await self.ignored_channel_commands(client, message)

    @classmethod
    async def enable_all_commands_with_send_logs(self, client, message):
        await self.enable_all_commands(client, message)
        await BotLogs.BotLogs.send_logs(client, message)

    @classmethod
    async def enable_all_commands_with_logs(self, client, message):
        await self.enable_all_commands(client, message)
        if _logging == 'True':
            BotLogs.BotLogs.logs(client, message)

    @classmethod
    async def pm_commands(self, client, message):
        await BotCommands.BotCommands.scan_for_invite_url_only_pm(client, message)
        await BotCommands.BotCommands.invite(client, message)
        await BotCommands.BotCommands.kills(client, message)
        await BotCommands.BotCommands.games(client, message)
        await BotCommands.BotCommands.other_commands(client, message)
        await BotCommands.BotCommands.bot_say(client, message)
        await BotCommands.BotCommands.randomcoin(client, message)
        await BotCommands.BotCommands.convert_url(client, message)
        if _logging == 'True':
            BotLogs.BotLogs.logs(client, message)

    @classmethod
    async def cheesy_commands(self, client, message):
        await self.enable_all_commands_with_logs(client, message)
        if message.content == "May I have access to the lab? I've agreed to the cheesy terms.":
            if message.author.id in newlyjoinedlist:
                role = discord.utils.find(lambda role: role.name == '🐀 LAB RATS', message.channel.server.roles)
                await client.send_message(message.channel, message.author.mention + ' You are now verified.')
                await client.add_roles(message.author, role)
                newlyjoinedlist.remove(message.author.id)


class BotIgnores:
    def __init__(self, client):
        self.bot = client

    @classmethod
    async def ignore(self, client, message):
        if message.channel.id not in somedict['channels']:
            # noinspection PyUnusedLocal
            try:
                if message.channel.is_private is not False:
                    # noinspection PyTypeChecker,PyCallByClass
                    await BotCommandData.pm_commands(client, message)
                elif message.channel.server and message.channel.server.id == "81812480254291968":
                    if message.author.id == bot_id:
                        return
                    elif message.channel.id == "153055192873566208":
                        # noinspection PyTypeChecker,PyCallByClass
                        await BotCommandData.enable_all_commands(client, message)
                    elif message.channel.id == "87382611688689664":
                        # noinspection PyTypeChecker,PyCallByClass
                        await BotCommandData.enable_all_commands(client, message)
                    else:
                        # noinspection PyTypeChecker,PyCallByClass
                        await BotCommandData.enable_all_commands_with_send_logs(client, message)
                elif message.channel.server and message.channel.server.id == "71324306319093760":
                    if message.channel.id == '141489876200718336':
                        # noinspection PyCallByClass,PyTypeChecker
                        await BotCommandData.cheesy_commands(client, message)
                    else:
                        # noinspection PyCallByClass,PyTypeChecker
                        await BotCommandData.enable_all_commands_with_logs(client, message)
                else:
                    # noinspection PyTypeChecker,PyCallByClass
                    await BotCommandData.enable_all_commands_with_logs(client, message)
            except Exception as e:
                if discord_user_id is not None:
                    owner = discord_user_id
                    exception_data = str(traceback.format_exc())
                    try:
                        await client.send_message(discord.User(id=owner), '```py\n' + exception_data + "\n```")
                    except discord.errors.Forbidden:
                        return
                else:
                    return
        else:
            # noinspection PyTypeChecker,PyCallByClass
            await BotCommandData.ignored_channel_commands(client, message)


class BotEvents:
    async def _resolve_delete_method(client, message):
        if message.channel.is_private is not False:
            if _logging == 'True':
                BotLogs.BotLogs.delete_logs(client, message)
        elif message.channel.server and message.channel.server.id == "81812480254291968":
            if message.author.id == bot_id:
                return
            elif message.channel.id == "153055192873566208":
                return
            elif message.channel.id == "87382611688689664":
                return
            else:
                await BotLogs.BotLogs.send_delete_logs(client, message)
        else:
            if message.channel.is_private is not False:
                return
            elif message.channel.server.id == '95342850102796288':
                return
            else:
                if _logging == 'True':
                    BotLogs.BotLogs.delete_logs(client, message)

    async def _resolve_edit_method(client, before, after):
        if before.channel.is_private is not False:
            if _logging == 'True':
                BotLogs.BotLogs.edit_logs(client, before, after)
        elif before.channel.server and before.channel.server.id == "81812480254291968":
            if before.author.id == bot_id:
                return
            elif before.channel.id == "153055192873566208":
                return
            elif before.channel.id == "87382611688689664":
                return
            else:
                await BotLogs.BotLogs.send_edit_logs(client, before, after)
        else:
            if before.channel.is_private is not False:
                return
            elif before.channel.server.id == '95342850102796288':
                return
            else:
                if _logging == 'True':
                    BotLogs.BotLogs.edit_logs(client, before, after)

    async def _resolve_onban(client, member):
        if _logbans == 'True':
            await BotLogs.BotLogs.onban(client, member)

    async def _resolve_onunban(client, user):
        if _logunbans == 'True':
            await BotLogs.BotLogs.onunban(client, user)

    async def _resolve_onremove(client, member):
        try:
            banslist = await client.get_bans(member.server)
            if member in banslist:
                return
            else:
                if _logkicks == 'True':
                    await BotLogs.BotLogs.onkick(client, member)
        except discord.errors.Forbidden:
            if _logkicks == 'True':
                await BotLogs.BotLogs.onkick(client, member)

    async def _resolve_onjoin(client, member):
        if member.server.id == '71324306319093760':
            message_part1 = "<@" + str(member.id) + '> has joined ' + member.server.name + '. Please Read the '
            message_part2 = message_part1 + "Code of Conduct in <#149323474765217792> and when you agree send the"
            message_part3 = message_part2 + "  command in here."
            message_data = message_part3
            await client.send_message(discord.Object(id='141489876200718336'), message_data)
            newlyjoinedlist.append(member.id)

    async def _resolve_on_login_voice_channel_join(client):
        # removed.
        # await BotCommands.BotCommands._reload_commands_bypass3(client)
        # added.
        await BotVoiceCommands.VoiceBotCommands._reload_commands_bypass3_new(client)
