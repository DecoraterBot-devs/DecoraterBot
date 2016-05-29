# coding=utf-8
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
import platform
# noinspection PyPackageRequirements
import youtube_dl
import time
import cmath
import ctypes
import subprocess
from threading import Timer
from collections import deque
import BotPMError
from discord.ext import commands

try:
    consoledatafile = io.open(sys.path[0] + '\\resources\\ConfigData\\ConsoleWindow.json', 'r')
    consoletext = json.load(consoledatafile)
except FileNotFoundError:
    print('ConsoleWindow.json is not Found. Cannot Continue.')
    sys.exit(2)
try:
    # noinspection PyPackageRequirements
    import TinyURL
    disabletinyurl = False
except ImportError:
    print_data_001 = 'TinyURL for Python 3.x was not installed.\n'
    print_data_002 = 'It can be found at: https://github.com/AraHaan/TinyURL\n'
    print_data_003 = 'Disabled the tinyurl command for now.'
    print(print_data_001 + print_data_002 + print_data_003)
    disabletinyurl = True
botbanslist = io.open(sys.path[0] + '\\resources\\ConfigData\\BotBanned.json', 'r')
banlist = json.load(botbanslist)
try:
    commandslist = io.open(sys.path[0] + '\\resources\\ConfigData\\BotCommands.json', 'r')
    commandlist = json.load(commandslist)
except FileNotFoundError:
    print(str(consoletext['Missing_JSON_Errors'][3]))
    sys.exit(2)
try:
    botmessagesdata = io.open(sys.path[0] + '\\resources\\ConfigData\\BotMessages.json', 'r')
    botmessages = json.load(botmessagesdata)
except FileNotFoundError:
    print(str(consoletext['Missing_JSON_Errors'][1]))
    sys.exit(2)

# Originally part of OtherCommands.py
version = str(consoletext['WindowVersion'][0])
rev = str(consoletext['Revision'][0])
sourcelink = str(botmessages['source_command_data'][0])
othercommands = str(botmessages['commands_command_data'][1])
commandstuff = str(botmessages['commands_command_data'][4])
botcommands = str(botmessages['commands_command_data'][0]) + othercommands + commandstuff
botcommands_without_other_stuff = str(botmessages['commands_command_data'][0]) + othercommands
othercommandthings = str(botmessages['commands_command_data'][4]) + str(botmessages['commands_command_data'][5])
botcommandswithturl_01 = str(botmessages['commands_command_data'][3]) + othercommandthings
botcommandswithtinyurl = botcommands_without_other_stuff + botcommandswithturl_01
changelog = str(botmessages['changelog_data'][0])
info = "``" + str(consoletext['WindowName'][0]) + version + rev + "``"
botcommandsPM = str(botmessages['commands_command_data'][2])
commandturlfix = str(botmessages['commands_command_data'][5])
botcommandsPMwithtinyurl = botcommandsPM + str(botmessages['commands_command_data'][3]) + commandturlfix
PATH = sys.path[0] + '\\resources\\ConfigData\\Credentials.json'

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    credsfile = io.open(PATH, 'r')
    credentials = json.load(credsfile)
    owner_id = str(credentials['ownerid'][0])
    _log_games = str(credentials['loggames'][0])
    _is_official_bot = str(credentials['Is_Official_Bot_Account'][0])
    _pm_commands_list = str(credentials['PM_Commands'][0])
    _bot_prefix = str(credentials['bot_prefix'][0])
    if _pm_commands_list == 'True':
        _pm_commands_list = True
    elif _pm_commands_list == 'False':
        _pm_commands_list = False

# noinspection PyUnboundLocalVariable
if _log_games == 'True':
    import BotLogs


class BotCommands:
    __slots__ = ['bot']

    def __init__(self, client):
        self.bot = client

    # Originally Attack.py
    @classmethod
    async def attack(self, client, message):
        self.bot = client
        if message.content.startswith(_bot_prefix + 'attack'):
            if message.author.id in banlist['Users']:
                return
            else:
                for user in message.mentions:
                    await self.bot.send_message(user, str(botmessages['attack_command_data'][0]))
                    break
                else:
                    await self.bot.send_message(message.author, str(botmessages['attack_command_data'][1]))

    # Originally ClearLogs.py
    # noinspection PyUnusedLocal
    @classmethod
    async def clear_logs(self, client, message):
        if message.content.lower().startswith(_bot_prefix + "info"):
            global fileviewmode
            logfile = 'log.txt'
            try:
                with open(logfile, 'r', encoding='utf-8') as file:
                    fileviewmode = True
                    size = os.path.getsize(logfile)
                    filecontent = file.read(size)
                    count_lines = 0
                for line in filecontent:
                    fixedline = line
                    if 'Name=' in fixedline:
                        count_lines = count_lines + 1
                    # if the line does not contains "Name=" then it must have logged a message that had more than 1 line
                    # in the first place. We got to check this for a accorate cache message count.
                    if fixedline == '':
                        fileviewmode = False
                        file.close()
                        constant = str(count_lines)
                        await self.bot.send_message(message.channel,
                                                    str(botmessages['info_command_data'][0]) + constant)
                        break
            except PermissionError:
                return
            except io.UnsupportedOperation:
                await self.bot.send_message(message.channel, str(botmessages['info_command_data'][1]))
        if message.content.startswith(_bot_prefix + "clear"):
            if message.author.id == message.channel.server.owner.id or owner_id:
                # clears the log.
                logfile = 'log.txt'
                try:
                    file = io.open(logfile, 'a', encoding='utf-8')
                    file.seek(0)
                    file.truncate()
                    await self.bot.send_message(message.channel, str(botmessages['clear_logs_command_data'][0]))
                except PermissionError:
                    return
            else:
                await self.bot.send_message(message.channel, str(botmessages['clear_logs_command_data'][1]))

    # Originally Coin.py
    @classmethod
    async def randomcoin(self, client, message):
        if message.content.startswith(_bot_prefix + 'coin'):
            if message.author.id in banlist['Users']:
                return
            else:
                msg = random.randint(0, 1)
                if msg == 0:
                    heads_coin = sys.path[0] + "\\resources\\images\\coins\\Heads.png"
                    try:
                        await self.bot.send_file(message.channel, heads_coin)
                    except discord.errors.Forbidden:
                        try:
                            message_data = 'This bot does not have Permission to Attach Files.'
                            await self.bot.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                if msg == 1:
                    tails_coin = sys.path[0] + "\\resources\\images\\coins\\Tails.png"
                    try:
                        await self.bot.send_file(message.channel, tails_coin)
                    except discord.errors.Forbidden:
                        try:
                            message_data = 'This bot does not have Permission to Attach Files.'
                            await self.bot.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)

    # Originally Colors.py
    @classmethod
    async def colors(self, client, message):
        if message.content.startswith(_bot_prefix + 'color'):
            if message.author.id in banlist['Users']:
                return
            else:
                if _bot_prefix + "pink" in message.content:
                    desrole = message.content[len(_bot_prefix + "color " + _bot_prefix + "pink "):].strip()
                    role = discord.utils.find(lambda role: role.name == desrole, message.channel.server.roles)
                    try:
                        await self.bot.edit_role(message.channel.server, role, color=discord.Colour(int('ff3054', 16)))
                    except discord.errors.Forbidden:
                        try:
                            message_data = 'This bot does not have permission to edit roles.'
                            await self.bot.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    except discord.errors.HTTPException:
                        return
                    except AttributeError:
                        return
                if _bot_prefix + "brown" in message.content:
                    desrole = message.content[len(_bot_prefix + "color " + _bot_prefix + "brown "):].strip()
                    role = discord.utils.find(lambda role: role.name == desrole, message.channel.server.roles)
                    try:
                        await self.bot.edit_role(message.channel.server, role, color=discord.Colour(int('652d2d', 16)))
                    except discord.errors.Forbidden:
                        try:
                            message_data = 'This bot does not have permission to edit roles.'
                            await self.bot.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    except discord.errors.HTTPException:
                        return
                    except AttributeError:
                        return

    # Originally Debug.py
    @classmethod
    async def debug(self, client, message):
        if message.content.startswith(_bot_prefix + 'eval'):
            if message.author.id == owner_id:
                debugcode = message.content[len(_bot_prefix + "eval "):].strip()
                if debugcode.rfind('await client.send_message(message.channel, ') is not -1:
                    debugcode = debugcode[len("await client.send_message(message.channel, "):].strip()
                    debugcode = debugcode.strip(")")
                    if debugcode.find("'") is not -1:
                        debugcode = debugcode.strip("'")
                    elif debugcode.find('"') is not -1:
                        debugcode = debugcode.strip('"')
                    if debugcode.find('message.author.mention') is not -1:
                        debugcode = debugcode.replace('message.author.mention + "', message.author.mention)
                    await self.bot.send_message(message.channel, debugcode)
                else:
                    botowner = discord.utils.find(lambda member: member.id == owner_id, message.channel.server.members)
                    # noinspection PyUnusedLocal
                    try:
                        try:
                            debugcode = eval(debugcode)
                        except SystemExit:
                            pass
                        debugcode = str(debugcode)
                        try:
                            await self.bot.send_message(message.channel, "```py\n" + debugcode + "\n```")
                        except discord.errors.Forbidden:
                            otherdata = " does not allow this bot to send"
                            msgdata = "Server owner of " + message.channel.server.name + otherdata
                            message_data = msgdata + " messages in " + message.channel.name + "."
                            await self.bot.send_message(botowner, message_data)
                            await self.bot.send_message(botowner, "```py\n" + debugcode + "\n```")
                    except Exception as e:
                        debugcode = traceback.format_exc()
                        debugcode = str(debugcode)
                        try:
                            await self.bot.send_message(message.channel, "```py\n" + debugcode + "\n```")
                        except discord.errors.Forbidden:
                            otherdata = " does not allow this bot to send"
                            msgdata = "Server owner of " + message.channel.server.name + otherdata
                            message_data = msgdata + " messages in " + message.channel.name + "."
                            await self.bot.send_message(botowner, message_data)
                            await self.bot.send_message(botowner, "```py\n" + debugcode + "\n```")
            else:
                try:
                    await self.bot.send_message(message.channel,
                                                "Sorry, Only my owner can eval Python Code. :eggplant:")
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'debug'):
            if message.author.id == owner_id:
                # added "# coding=utf-8" to this to bypass the error on "No Encoding specified for file."
                debugcode_new = "# coding=utf-8\n" + message.content[len(_bot_prefix + "debug "):].strip()
                # noinspection PyPep8Naming
                BotOwner = discord.utils.find(lambda member: member.id == owner_id, message.channel.server.members)
                # noinspection PyUnusedLocal
                try:
                    evalcodefile = sys.path[0] + '\\resources\\exec_files\\exec_temp.py'
                    eval_temp_code = io.open(evalcodefile, 'w+', encoding='utf-8')
                    # to bypass PEP8: No new line at end of file.
                    debugcode_new = debugcode_new + '\n'
                    eval_temp_code.write(debugcode_new)
                    eval_temp_code.close()
                    execoutputfile = sys.path[0] + '\\resources\\exec_files\\eval_output_temp.txt'
                    eval_temp_result_output = io.open(execoutputfile, 'w', encoding='utf-8')
                    out = eval_temp_result_output
                    p = subprocess.Popen(sys.path[4] + "\\python " + evalcodefile, stdout=out, stderr=out, shell=True)
                    p.wait()
                    # time.sleep(10)
                    eval_temp_result_output.close()
                    eval_temp_result_read = io.open(execoutputfile, 'r', encoding='utf-8')
                    eval_result = eval_temp_result_read.read()
                    if eval_result is not '':
                        debugcode = eval_result
                    else:
                        debugcode = 'None'
                    eval_temp_result_read.close()
                    try:
                        await self.bot.send_message(message.channel, "```py\n" + debugcode + "\n```")
                    except discord.errors.Forbidden:
                        msgdata = "Server owner of " + message.channel.server.name + " does not allow this bot to send"
                        message_data = msgdata + " messages in " + message.channel.name + "."
                        await self.bot.send_message(BotOwner, message_data)
                        await self.bot.send_message(BotOwner, "```py\n" + debugcode + "\n```")
                except Exception as e:
                    debugcode = traceback.format_exc()
                    debugcode = str(debugcode)
                    try:
                        await self.bot.send_message(message.channel, "```py\n" + debugcode + "\n```")
                    except discord.errors.Forbidden:
                        msgdata = "Server owner of " + message.channel.server.name + " does not allow this bot to send"
                        message_data = msgdata + " messages in " + message.channel.name + "."
                        await self.bot.send_message(BotOwner, message_data)
                        await self.bot.send_message(BotOwner, "```py\n" + debugcode + "\n```")
            else:
                try:
                    await self.bot.send_message(message.channel,
                                                "Sorry, Only my owner can debug Python Code. :eggplant:")
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)

    # Originally Games.py
    @classmethod
    async def games(self, client, message):
        if message.content.startswith(_bot_prefix + 'game'):
            if message.author.id in banlist['Users']:
                return
            else:
                desgame = message.content[len(_bot_prefix + "game "):].strip()
                desgametype = None
                stream_url = None
                if len(desgame) > 0:
                    if len(message.mentions) > 0:
                        for x in message.mentions:
                            desgame = desgame.replace(x.mention, x.name)
                    desgame = str(desgame)
                    if desgame.find(" | type=") is not -1:
                        if desgame.find(" | type=1") is not -1:
                            desgame = desgame.replace(" | type=1", "")
                            desgametype = 1
                            stream_url = "https://twitch.tv/decoraterbot"
                        elif desgame.find(" | type=2") is not -1:
                            desgame = desgame.replace(" | type=2", "")
                            desgametype = 2
                            stream_url = "https://twitch.tv/decoraterbot"
                    if desgametype is not None:
                        if _log_games == 'True':
                            BotLogs.BotLogs.gamelog(client, message, desgame)
                        await self.bot.change_status(game=discord.Game(name=desgame, type=desgametype, url=stream_url))
                        try:
                            msgdata = str(botmessages['game_command_data'][0]).format(desgame)
                            message_data = msgdata.replace("idle", "streaming")
                            await self.bot.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    else:
                        if _log_games == 'True':
                            BotLogs.BotLogs.gamelog(client, message, desgame)
                        await self.bot.change_status(game=discord.Game(name=desgame), idle=True)
                        try:
                            msgdata = str(botmessages['game_command_data'][0]).format(desgame)
                            message_data = msgdata
                            await self.bot.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'remgame'):
            if message.author.id in banlist['Users']:
                return
            else:
                game_name = str(consoletext['On_Ready_Game'][0])
                stream_url = "https://twitch.tv/decoraterbot"
                await client.change_status(game=discord.Game(name=game_name, type=1, url=stream_url))
                try:
                    await self.bot.send_message(message.channel, str(botmessages['remgame_command_data'][0]))
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)

    # Originally Invite.py
    # noinspection PyUnusedLocal
    @classmethod
    async def invite(self, client, message):
        if message.content.startswith(_bot_prefix + 'join'):
            if message.author.id in banlist['Users']:
                return
            else:
                if _is_official_bot == 'True':
                    await self.bot.send_message(message.channel, str(botmessages['join_command_data'][3]))
                else:
                    code = message.content[len(_bot_prefix + "join "):].strip()
                    if code == '':
                        url = None
                    else:
                        url = code
                    if url is not None:
                        try:
                            await self.bot.accept_invite(url)
                            await self.bot.send_message(message.channel, str(botmessages['join_command_data'][0]))
                        except discord.errors.NotFound:
                            await self.bot.send_message(message.channel, str(botmessages['join_command_data'][1]))
                    else:
                        await self.bot.send_message(message.channel, str(botmessages['join_command_data'][2]))

    # Originally Kills.py
    @classmethod
    async def kills(self, client, message):
        if message.content.startswith(_bot_prefix + 'kill'):
            if message.author.id in banlist['Users']:
                return
            else:
                data = message.content[len(_bot_prefix + "kill "):].strip()
                if message.channel.is_private is not False:
                    msg = random.randint(1, 4)
                    if msg == 1:
                        message_data = str(botmessages['kill_command_data'][0]).format(message.author)
                        await self.bot.send_message(message.channel, message_data)
                    if msg == 2:
                        message_data = str(botmessages['kill_command_data'][1]).format(message.author)
                        await self.bot.send_message(message.channel, message_data)
                    if msg == 3:
                        message_data = str(botmessages['kill_command_data'][2]).format(message.author)
                        await self.bot.send_message(message.channel, message_data)
                    if msg == 4:
                        message_data = str(botmessages['kill_command_data'][3]).format(message.author)
                        await self.bot.send_message(message.channel, message_data)
                else:
                    if data.rfind(self.bot.user.name) != -1:
                        try:
                            await self.bot.send_message(message.channel, str(botmessages['kill_command_data'][4]))
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    else:
                        msg = random.randint(1, 4)
                        for disuser in message.mentions:
                            if message.author == disuser:
                                try:
                                    await self.bot.send_message(message.channel,
                                                                str(botmessages['kill_command_data'][4]))
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                                break
                            if self.bot.user == disuser:
                                try:
                                    await self.bot.send_message(message.channel,
                                                                str(botmessages['kill_command_data'][4]))
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                                break
                            user = discord.utils.find(lambda member: member.name == disuser.name,
                                                      message.channel.server.members)
                            if msg == 1:
                                try:
                                    msgdata = str(botmessages['kill_command_data'][5]).format(message.author, user)
                                    message_data = msgdata
                                    await self.bot.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                                break
                            if msg == 2:
                                try:
                                    msgdata = str(botmessages['kill_command_data'][6]).format(message.author, user)
                                    message_data = msgdata
                                    await self.bot.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                                break
                            if msg == 3:
                                try:
                                    msgdata = str(botmessages['kill_command_data'][7]).format(message.author, user)
                                    message_data = msgdata
                                    await self.bot.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                                break
                            if msg == 4:
                                try:
                                    msgdata = str(botmessages['kill_command_data'][8]).format(message.author, user)
                                    message_data = msgdata
                                    await self.bot.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                                break
                        else:
                            if msg == 1:
                                try:
                                    message_data = str(botmessages['kill_command_data'][0]).format(message.author)
                                    await self.bot.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                            if msg == 2:
                                try:
                                    message_data = str(botmessages['kill_command_data'][1]).format(message.author)
                                    await self.bot.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                            if msg == 3:
                                try:
                                    message_data = str(botmessages['kill_command_data'][2]).format(message.author)
                                    await self.bot.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                            if msg == 4:
                                try:
                                    message_data = str(botmessages['kill_command_data'][3]).format(message.author)
                                    await self.bot.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)

    # Originally Moderator.py
    @classmethod
    async def mod_commands(self, client, message):
        if len(message.mentions) > 5:
            await self.mention_ban_helper(client, message)
        if message.content.startswith(_bot_prefix + "ban"):
            if message.author.id == message.channel.server.owner.id or owner_id:
                for disuser in message.mentions:
                    listdata = message.channel.server.members
                    member = discord.utils.find(lambda member: member.name == disuser.name, listdata)
                    try:
                        await self.bot.ban(member, delete_message_days=7)
                        try:
                            message_data = str(botmessages['ban_command_data'][0]).format(member)
                            await self.bot.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                        break
                    except discord.Forbidden:
                        try:
                            await self.bot.send_message(message.channel, str(botmessages['ban_command_data'][1]))
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    except discord.HTTPException:
                        try:
                            await self.bot.send_message(message.channel, str(botmessages['ban_command_data'][2]))
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                else:
                    try:
                        await self.bot.send_message(message.channel, str(botmessages['ban_command_data'][3]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
            else:
                try:
                    await client.send_message(message.channel, str(botmessages['ban_command_data'][4]))
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + "softban"):
            if message.author.id == message.channel.server.owner.id or owner_id:
                for disuser in message.mentions:
                    memberlist = message.channel.server.members
                    member = discord.utils.find(lambda member: member.name == disuser.name, memberlist)
                    try:
                        await self.bot.ban(member, delete_message_days=7)
                        await self.bot.unban(member.server, member)
                        try:
                            message_data = str(botmessages['softban_command_data'][0]).format(member)
                            await self.bot.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                        break
                    except discord.Forbidden:
                        try:
                            await self.bot.send_message(message.channel, str(botmessages['softban_command_data'][1]))
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    except discord.HTTPException:
                        try:
                            await self.bot.send_message(message.channel, str(botmessages['softban_command_data'][2]))
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                else:
                    try:
                        await self.bot.send_message(message.channel, str(botmessages['softban_command_data'][3]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
            else:
                try:
                    await self.bot.send_message(message.channel, str(botmessages['softban_command_data'][4]))
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + "kick"):
            if message.author.id == message.channel.server.owner.id or owner_id:
                for disuser in message.mentions:
                    memberlist = message.channel.server.members
                    member = discord.utils.find(lambda member: member.name == disuser.name, memberlist)
                    try:
                        await self.bot.kick(member)
                        try:
                            message_data = str(botmessages['kick_command_data'][0]).format(member)
                            await self.bot.send_message(message.channel, message_data)
                            break
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                        break
                    except discord.Forbidden:
                        try:
                            await self.bot.send_message(message.channel, str(botmessages['kick_command_data'][1]))
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    except discord.HTTPException:
                        try:
                            await self.bot.send_message(message.channel, str(botmessages['kick_command_data'][2]))
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                else:
                    try:
                        await self.bot.send_message(message.channel, str(botmessages['kick_command_data'][3]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
            else:
                try:
                    await self.bot.send_message(message.channel, str(botmessages['kick_command_data'][4]))
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)

    # Originally OtherCommands.py
    @classmethod
    async def other_commands(self, client, message):
        if message.content.startswith(_bot_prefix + 'commands'):
            if message.author.id in banlist['Users']:
                return
            else:
                if message.channel.is_private is not False:
                    if disabletinyurl is True:
                        await self.bot.send_message(message.channel, botcommandsPM)
                    else:
                        await self.bot.send_message(message.channel, botcommandsPMwithtinyurl)
                else:
                    if disabletinyurl is True:
                        try:
                            if _pm_commands_list is True:
                                await self.bot.send_message(message.author, botcommands)
                            else:
                                await self.bot.send_message(message.channel, botcommands)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    else:
                        try:
                            if _pm_commands_list is True:
                                await self.bot.send_message(message.author, botcommandswithtinyurl)
                                msgdata = message.author.mention + ' ``Ok, check your private messages`` '
                                message_data = msgdata + ':thumbsup:'
                                try:
                                    await self.bot.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                            else:
                                await self.bot.send_message(message.channel, botcommandswithtinyurl)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'changelog'):
            if message.author.id in banlist['Users']:
                return
            else:
                try:
                    await self.bot.send_message(message.channel, changelog.format(version + rev))
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'raid'):
            if message.author.id in banlist['Users']:
                return
            else:
                if message.channel.is_private is not False:
                    return
                else:
                    result = message.content.replace("::raid ", "")
                    try:
                        message_data = str(botmessages['raid_command_data'][0]).format(result)
                        await self.bot.send_message(message.channel, message_data)
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'update'):
            if message.author.id in banlist['Users']:
                return
            else:
                if message.channel.is_private is not False:
                    return
                else:
                    try:
                        await self.bot.send_message(message.channel, str(botmessages['update_command_data'][0]).format(info))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'Libs'):
            if message.author.id in banlist['Users']:
                return
            else:
                libs = str(botmessages['Libs_command_data'][0])
                try:
                    await self.bot.send_message(message.channel, libs)
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'source'):
            if message.author.id in banlist['Users']:
                return
            else:
                try:
                    msgdata = sourcelink.format(message.author)
                    message_data = msgdata
                    await self.bot.send_message(message.channel, message_data)
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'type'):
            if message.author.id in banlist['Users']:
                return
            else:
                await self.bot.send_typing(message.channel)
        if message.content.startswith(_bot_prefix + 'pyversion'):
            if message.author.id in banlist['Users']:
                return
            else:
                if message.channel.is_private is not False:
                    return
                else:
                    if bits == 8:
                        python_platform = "64-Bit"
                    elif bits == 4:
                        python_platform = "32-Bit"
                    # noinspection PyUnboundLocalVariable
                    vers = "```py\nPython v" + platform.python_version() + " " + python_platform + "```"
                    try:
                        await self.bot.send_message(message.channel, vers)
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'AgarScrub'):
            try:
                reply = 'https://imgflip.com/i/12yq2n'
                await self.bot.send_message(message.channel, reply)
            except discord.errors.Forbidden:
                await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'stats'):
            server_count = str(len(self.bot.servers))
            member_count = str(len(set([member for member in self.bot.get_all_members()])))
            textchannels_count = str(len(set([channel for channel in self.bot.get_all_channels() if channel.type == discord.ChannelType.text])))
            formatted_data = str(botmessages['stats_command_data'][0]).format(server_count, member_count, textchannels_count)
            await self.bot.send_message(message.channel, formatted_data)
        if message.content.startswith(_bot_prefix + 'rs'):
            filename = str(sys.path[0]) + '\\resources\images\elsword\\RS.jpg'
            file_object = open(filename, 'rb')
            if file_object is not None:
                file_data = file_object.read()
                file_object.close()
            # noinspection PyUnboundLocalVariable
            await self.bot.edit_profile(avatar=file_data)
        if message.content.startswith(_bot_prefix + 'as'):
            filename = str(sys.path[0]) + '\\resources\images\elsword\\AS.jpg'
            file_object = open(filename, 'rb')
            if file_object is not None:
                file_data = file_object.read()
                file_object.close()
            await self.bot.edit_profile(avatar=file_data)
        if message.content.startswith(_bot_prefix + 'ai'):
            filename = str(sys.path[0]) + '\\resources\images\elsword\\AI.jpg'
            file_object = open(filename, 'rb')
            if file_object is not None:
                file_data = file_object.read()
                file_object.close()
            await self.bot.edit_profile(avatar=file_data)
        """
            This below is left in so anyone could have a example of itterating through roles to find the right one that
            they want.

            Note: This uses the json module to load up ppl who was listed in a json file that cannot use the bot.

            if message.content.startswith(_bot_prefix + 'roleinfo'):
                if message.author.id in banlist['Users']:
                    message_data = " Due to Continuous abuse you have been Bot Banned."
                    await self.bot.send_message(message.channel, message.author.mention + message_data)
                else:
                    for role in message.channel.server.roles:
                        await self.bot.send_message(message.channel,
                        "``role name: {0.role.name}, role id: {1.role.id}``")
        """

    # Originally Prune.py
    @classmethod
    async def prune(self, client, message):
        global sent_prune_error_message
        if message.content.startswith(_bot_prefix + 'prune'):
            if message.author.id in banlist['Users']:
                return
            else:
                role = discord.utils.find(lambda role: role.name == 'Bot Commander', message.channel.server.roles)
                #                if message.author.id == owner_id:
                #                    opt = message.content[len(_bot_prefix + "prune "):].strip()
                #                    num = 1
                #                    if opt:
                #                        try:
                #                            num = int(opt)
                #                        except:
                #                            return
                #                    async for msg in self.bot.logs_from(message.channel, limit=num + 1):
                #                        try:
                #                            await self.bot.delete_message(msg)
                #                        except discord.HTTPException:
                #                            await self.bot.send_message(message.channel,
                #                                                       str(botmessages['prune_command_data'][0]))
                #                else:
                if role in message.author.roles:
                    opt = message.content[len(_bot_prefix + "prune "):].strip()
                    num = 1
                    if opt:
                        try:
                            num = int(opt)
                        except:
                            return
                    async for msg in self.bot.logs_from(message.channel, limit=num + 1):
                        try:
                            await self.bot.delete_message(msg)
                        except discord.HTTPException:
                            if sent_prune_error_message is False:
                                sent_prune_error_message = True
                                await self.bot.send_message(message.channel, str(botmessages['prune_command_data'][0]))
                            else:
                                return
                                # except discord.errors.RateLimitError
                else:
                    try:
                        await self.bot.send_message(message.channel, str(botmessages['prune_command_data'][1]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)

    # Originally Roles.py
    @classmethod
    async def bot_roles(self, client, message):
        if message.content.startswith(_bot_prefix + 'giveme'):
            if message.channel.server and message.channel.server.id == "81812480254291968":
                desrole = message.content[len(_bot_prefix + "giveme "):].strip()
                role = discord.utils.find(lambda role: role.name == 'Muted', message.channel.server.roles)
                role3 = discord.utils.find(lambda role: role.name == 'Students', message.channel.server.roles)
                if 'admin' in desrole:
                    if 'Muted' in message.author.roles:
                        await self.bot.add_roles(message.author, role)
                        await self.bot.send_message(message.channel, str(botmessages['giveme_command_data'][0]))
                    else:
                        await self.bot.send_message(message.channel, str(botmessages['giveme_command_data'][5]))
                elif 'student' in desrole:
                    if 'Students' in message.author.roles:
                        await self.bot.add_roles(message.author, role3)
                        await self.bot.send_message(message.channel, str(botmessages['giveme_command_data'][1]))
                    else:
                        await self.bot.send_message(message.channel, str(botmessages['giveme_command_data'][6]))
            else:
                if message.channel.server and message.channel.server.id == "127233852182626304":
                    desrole = message.content[len(_bot_prefix + "giveme "):].strip()
                    rolelist = message.channel.server.roles
                    role = discord.utils.find(lambda role: role.name == '3rd Party Developer', rolelist)
                    role3 = discord.utils.find(lambda role: role.name == 'Streamer', rolelist)
                    if 'dev' in desrole:
                        if role not in message.author.roles:
                            await client.add_roles(message.author, role)
                            await client.send_message(message.channel, str(botmessages['giveme_command_data'][2]))
                        else:
                            await client.send_message(message.channel, str(botmessages['giveme_command_data'][7]))
                    elif 'stream' in desrole:
                        if role3 not in message.author.roles:
                            await client.add_roles(message.author, role3)
                            await client.send_message(message.channel, str(botmessages['giveme_command_data'][3]))
                        else:
                            await client.send_message(message.channel, str(botmessages['giveme_command_data'][8]))
                else:
                    try:
                        await client.send_message(message.channel, str(botmessages['giveme_command_data'][4]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'remove'):
            if message.channel.server and message.channel.server.id == "127233852182626304":
                desrole = message.content[len(_bot_prefix + "remove "):].strip()
                rolelist = message.channel.server.roles
                role = discord.utils.find(lambda role: role.name == '3rd Party Developer', rolelist)
                role3 = discord.utils.find(lambda role: role.name == 'Streamer', rolelist)
                if 'dev' in desrole:
                    if role in message.author.roles:
                        await self.bot.remove_roles(message.author, role)
                        await self.bot.send_message(message.channel, str(botmessages['remove_command_data'][0]))
                    else:
                        await self.bot.send_message(message.channel, str(botmessages['remove_command_data'][2]))
                elif 'stream' in desrole:
                    if role3 in message.author.roles:
                        await self.bot.remove_roles(message.author, role3)
                        await self.bot.send_message(message.channel, str(botmessages['remove_command_data'][1]))
                    else:
                        await self.bot.send_message(message.channel, str(botmessages['remove_command_data'][3]))
            else:
                return

    # Originally Say.py
    @classmethod
    async def bot_say(self, client, message):
        if message.content.startswith(_bot_prefix + 'say'):
            if message.author.id in banlist['Users']:
                return
            else:
                say = message.content[len(_bot_prefix + "say "):].strip()
                if say.rfind(_bot_prefix) != -1:
                    message_data = str(botmessages['say_command_data'][0]).format(message.author)
                    await self.bot.send_message(message.channel, message_data)
                elif say.rfind("@") != -1:
                    message_data = str(botmessages['say_command_data'][1]).format(message.author)
                    await self.bot.send_message(message.channel, message_data)
                else:
                    try:
                        await self.bot.send_message(message.channel, say)
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
                    except discord.errors.HTTPException:
                        return

    @classmethod
    async def bot_mentioned_helper(self, client, message):
        if message.author.id in banlist['Users']:
            return
        elif message.author.bot is True:
            return
        else:
            pref = _bot_prefix
            unig = 'unignorechannel'
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
            elif message.content.startswith(pref + 'tinyurl') or message.content.startswith(pref + 'JoinVoiceChannel'):
                return
            elif message.content.startswith(pref + 'play') or message.content.startswith(pref + 'pause'):
                return
            elif message.content.startswith(pref + 'unpause') or message.content.startswith(pref + 'stop'):
                return
            elif message.content.startswith(pref + 'move') or message.content.startswith(pref + 'LeaveVoiceChannel'):
                return
            elif message.content.startswith(pref + 'Playlist'):
                    return
            else:
                if message.channel.server.id == "140849390079180800":
                    return
                elif message.author.id == self.bot.user.id:
                    return
                elif message.channel.server.id == "110373943822540800":
                    if message.author.id == "103607047383166976":
                        return
                    else:
                        info = str(botmessages['On_Bot_Mention_Message_Data'][0]).format(message.author)
                        await self.bot.send_message(message.channel, info)
                elif message.channel.server.id == '101596364479135744':
                    if message.author.id == "110368240768679936":
                        return
                    else:
                        info = str(botmessages['On_Bot_Mention_Message_Data'][0]).format(message.author)
                        await self.bot.send_message(message.channel, info)
                else:
                    info = str(botmessages['On_Bot_Mention_Message_Data'][0]).format(message.author)
                    try:
                        await self.bot.send_message(message.channel, info)
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)

    @classmethod
    async def mention_ban_helper(self, client, message):
        if message.author.id == self.bot.user.id:
            return
        if message.channel.server.id == "105010597954871296":
            return
        if message.author.id == owner_id:
            return
        else:
            try:
                await self.bot.ban(message.author)
                try:
                    message_data = str(botmessages['mention_spam_ban'][0]).format(message.author)
                    await self.bot.send_message(message.channel, message_data)
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)
            except discord.errors.Forbidden:
                try:
                    msgdata = str(botmessages['mention_spam_ban'][1]).format(message.author)
                    message_data = msgdata
                    await self.bot.send_message(message.channel, message_data)
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)
            except discord.HTTPException:
                try:
                    msgdata = str(botmessages['mention_spam_ban'][2]).format(message.author)
                    message_data = msgdata
                    await self.bot.send_message(message.channel, message_data)
                except discord.errors.Forbidden:
                    await BotPMError._resolve_send_message_error(client, message)

    # Originally SomeMoreCommands.py
    @classmethod
    async def more_commands(self, client, message):
        if self.bot.user.mention in message.content:
            await self.bot_mentioned_helper(client, message)
        elif message.content.startswith(_bot_prefix + "clear"):
            if message.author.id in banlist['Users']:
                return
            else:
                async for msg in self.bot.logs_from(message.channel, limit=100):
                    if msg.author.id == self.bot.user.id:
                        try:
                            await self.bot.delete_message(msg)
                        except discord.HTTPException:
                            return
        elif message.content.startswith(_bot_prefix + 'botban'):
            if message.author.id == owner_id:
                if len(message.mentions) < 1:
                    try:
                        await self.bot.send_message(message.channel, 'You must mention a user to Bot Ban.')
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
                else:
                    if message.mentions[0].id not in banlist['Users']:
                        try:
                            banlist['Users'].append(message.mentions[0].id)
                            json.dump(banlist, open(sys.path[0] + "\\resources\\ConfigData\\BotBanned.json", "w"))
                            # noinspection PyUnusedLocal
                            try:
                                message_data = str(botmessages['bot_ban_command_data'][0]).format(message.mentions[0])
                                await self.bot.send_message(message.channel, message_data)
                            except discord.errors.Forbidden:
                                await BotPMError._resolve_send_message_error(client, message)
                            except Exception as e:
                                try:
                                    messagedata = str(botmessages['bot_ban_command_data'][1]).format(message.mentions[0])
                                    message_data = messagedata + str(botmessages['bot_ban_command_data'][2])
                                    await self.bot.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    await BotPMError._resolve_send_message_error(client, message)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
        elif message.content.startswith(_bot_prefix + 'botunban'):
            if message.author.id == owner_id:
                if len(message.mentions) < 1:
                    try:
                        await self.bot.send_message(message.channel, 'You must mention a user to Bot Unban.')
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
                else:
                    if message.mentions[0].id in banlist['Users']:
                        # noinspection PyUnusedLocal
                        try:
                            tobotunban = banlist['Users']
                            tobotunban.remove(message.mentions[0].id)
                            json.dump(banlist, open(sys.path[0] + "\\resources\\ConfigData\\BotBanned.json", "w"))
                            try:
                                message_data = str(botmessages['bot_unban_command_data'][0]).format(message.mentions[0])
                                await self.bot.send_message(message.channel, message_data)
                            except discord.errors.Forbidden:
                                await BotPMError._resolve_send_message_error(client, message)
                        except Exception as e:
                            try:
                                messagedata = str(botmessages['bot_unban_command_data'][1]).format(message.mentions[0])
                                message_data = messagedata + str(botmessages['bot_unban_command_data'][2])
                                await self.bot.send_message(message.channel, message_data)
                            except discord.errors.Forbidden:
                                await BotPMError._resolve_send_message_error(client, message)

    # Originally Userinfo.py
    @classmethod
    async def userdata(self, client, message):
        if message.content.startswith(_bot_prefix + "userinfo"):
            if message.author.id in banlist['Users']:
                return
            else:
                # noinspection PyUnusedLocal
                for disuser in message.mentions:
                    username = message.mentions[0].name
                    seenin = set([member.server.name for member in self.bot.get_all_members()
                                  if member.name == username])
                    seenin = str(len(seenin))
                    if str(message.mentions[0].game) != 'None':
                        desuser = message.mentions[0]
                        msgdata_1 = str(botmessages['userinfo_command_data'][0]).format(desuser, seenin)
                        message_data = msgdata_1
                        data = message_data
                    else:
                        desuser = message.mentions[0]
                        msgdata_1 = str(botmessages['userinfo_command_data'][0]).format(desuser, seenin)
                        message_data = msgdata_1.replace("Playing ", "")
                        data = message_data
                    try:
                        await self.bot.send_message(message.channel, data)
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)
                    break
                else:
                    seenin = set([member.server.name for member in self.bot.get_all_members() if member.name ==
                                  message.author.name])
                    seenin = str(len(seenin))
                    if str(message.author.game) != 'None':
                        msgdata_1 = str(botmessages['userinfo_command_data'][0]).format(message.author, seenin)
                        message_data = msgdata_1
                        data = message_data
                    else:
                        msgdata_1 = str(botmessages['userinfo_command_data'][0]).format(message.author, seenin)
                        message_data = msgdata_1.replace("Playing ", "")
                        data = message_data
                    try:
                        await self.bot.send_message(message.channel, data)
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)

    # Originally ConvertURL.py from the Python 2.x version of this bot. (2.x version is dead)
    @classmethod
    async def convert_url(self, client, message):
        if message.content.startswith(_bot_prefix + 'tinyurl'):
            if disabletinyurl is True:
                return
            elif disabletinyurl is False:
                url = message.content[len(_bot_prefix + "tinyurl "):].strip()
                if '<' and '>' in url:
                    url = url.strip('<')
                    url = url.strip('>')
                if url != '':
                    if url.startswith("http://"):
                        link = TinyURL.TinyURL.create_one(url)
                        link = str(link)
                        result = str(botmessages['tinyurl_command_data'][0]).format(link)
                        try:
                            await self.bot.send_message(message.channel, result)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    else:
                        if url.startswith("https://"):
                            # do nothing
                            # noinspection PyUnusedLocal
                            do_nothing = None
                        elif url.startswith("ftp://"):
                            # do nothing
                            # noinspection PyUnusedLocal
                            do_nothing = None
                        else:
                            try:
                                await self.bot.send_message(message.channel,
                                                            str(botmessages['tinyurl_command_data'][1]))
                            except discord.errors.Forbidden:
                                await BotPMError._resolve_send_message_error(client, message)
                    if url.startswith("https://"):
                        link = TinyURL.TinyURL.create_one(url)
                        link = str(link)
                        result = str(botmessages['tinyurl_command_data'][0]).format(link)
                        try:
                            await self.bot.send_message(message.channel, result)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    else:
                        if url.startswith("ftp://"):
                            # do nothing
                            # noinspection PyUnusedLocal
                            do_nothing = None
                        elif url.startswith("http://"):
                            # do nothing
                            # noinspection PyUnusedLocal
                            do_nothing = None
                        else:
                            try:
                                await self.bot.send_message(message.channel,
                                                            str(botmessages['tinyurl_command_data'][1]))
                            except discord.errors.Forbidden:
                                await BotPMError._resolve_send_message_error(client, message)
                    if url.startswith("ftp://"):
                        link = TinyURL.TinyURL.create_one(url)
                        link = str(link)
                        result = str(botmessages['tinyurl_command_data'][0]).format(link)
                        try:
                            await self.bot.send_message(message.channel, result)
                        except discord.errors.Forbidden:
                            await BotPMError._resolve_send_message_error(client, message)
                    else:
                        if url.startswith("http://"):
                            # do nothing
                            # noinspection PyUnusedLocal
                            do_nothing = None
                        elif url.startswith("https://"):
                            # do nothing
                            # noinspection PyUnusedLocal
                            do_nothing = None
                        else:
                            try:
                                await self.bot.send_message(message.channel,
                                                            str(botmessages['tinyurl_command_data'][1]))
                            except discord.errors.Forbidden:
                                await BotPMError._resolve_send_message_error(client, message)
                else:
                    try:
                        await self.bot.send_message(message.channel, str(botmessages['tinyurl_command_data'][2]))
                    except discord.errors.Forbidden:
                        await BotPMError._resolve_send_message_error(client, message)

    # noinspection PyUnusedLocal
    @classmethod
    async def scan_for_invite_url_only_pm(self, client, message):
        if _is_official_bot == 'True':
            if message.content.startswith('https://discord.gg/'):
                await self.bot.send_message(message.channel, str(botmessages['join_command_data'][3]))
            if message.content.startswith('http://discord.gg/'):
                await self.bot.send_message(message.channel, str(botmessages['join_command_data'][3]))
