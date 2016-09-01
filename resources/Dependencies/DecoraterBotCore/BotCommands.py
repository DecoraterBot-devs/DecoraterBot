# coding=utf-8
"""
    DecoraterBot's source is protected by Cheese.lab industries Inc. Even though it is Open Source
    any and all users waive the right to say that this bot's code was stolen when it really was not.
    Me @Decorater the only core developer of this bot do not take kindly to those false Allegations.
    it would piss any DEVELOPER OFF WHEN THEY SPEND ABOUT A YEAR CODING STUFF FROM SCRATCH AND THEN BE ACCUSED OF
    CRAP LIKE THIS.
    
    So, do not do it. If you do Cheese.lab Industries Inc. Can and Will go after you for such cliams that it deems
    untrue.
    
    Cheese.lab industries Inc. Believes in the rights of Original Developers of bots. They do not take kindly to
    BULLCRAP.
    
    Any and all Developers work all the time, many of them do not get paid for their hard work.
    
    I am one of those who did not get paid even though I am the original Developer I coded this bot from the bottom
    with no lines of code at all.
    
    And how much money did I get from it for my 11 months or so of working on it? None, yeah thats right 0$ how
    pissed can someone get?
    Exactly I have over stretched my relatives money that they paid for Internet and power for my computer so that
    way I can code my bot.
    
    However crap does go out of the Fan with a possible 600$ or more that my Laptop Drastically needs to Repairs as
    it is 10 years old and is falling apart
    
    I am half tempted myself to pulling this bot from github and making it on patrion that boobot was on to help me
    with my development needs.
    
    So, as such I accept issue requests, but please do not give me bullcrap I hate it as it makes everything worse
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
import platform
import gc
import importlib
import youtube_dl
import aiohttp
import multidict
import setuptools
import time
import cmath
import ctypes
import subprocess
from threading import Timer
from collections import deque
# noinspection PyUnresolvedReferences
import BotPMError
# noinspection PyUnresolvedReferences
import py2pycx
from discord.ext import commands

sepa = os.sep

# noinspection PyGlobalUndefined
global sent_prune_error_message
# noinspection PyRedeclaration
sent_prune_error_message = False

bits = ctypes.sizeof(ctypes.c_voidp)
PY36 = sys.version_info >= (3, 6)
PY35 = sys.version_info >= (3, 5)

try:
    consoledatafile = io.open('{0}{1}resources{1}ConfigData{1}ConsoleWindow.json'.format(sys.path[0], sepa))
    consoletext = json.load(consoledatafile)
    consoledatafile.close()
except FileNotFoundError:
    print('ConsoleWindow.json is not Found. Cannot Continue.')
    sys.exit(2)
try:
    # noinspection PyUnresolvedReferences
    import TinyURL
    disabletinyurl = False
except ImportError:
    print_data_001 = 'TinyURL for Python 3.x was not installed.\n'
    print_data_002 = 'It can be found at: https://github.com/AraHaan/TinyURL\n'
    print_data_003 = 'Disabled the tinyurl command for now.'
    print(print_data_001 + print_data_002 + print_data_003)
    disabletinyurl = True
botbanslist = io.open('{0}{1}resources{1}ConfigData{1}BotBanned.json'.format(sys.path[0], sepa))
banlist = json.load(botbanslist)
botbanslist.close()
try:
    commandslist = io.open('{0}{1}resources{1}ConfigData{1}BotCommands.json'.format(sys.path[0], sepa))
    commandlist = json.load(commandslist)
    commandslist.close()
except FileNotFoundError:
    print(str(consoletext['Missing_JSON_Errors'][3]))
    sys.exit(2)
try:
    botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.json'.format(sys.path[0], sepa))
    botmessages = json.load(botmessagesdata)
    botmessagesdata.close()
except FileNotFoundError:
    print(str(consoletext['Missing_JSON_Errors'][1]))
    sys.exit(2)

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
PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(sys.path[0], sepa)

_log_games = True
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    credsfile = io.open(PATH)
    credentials = json.load(credsfile)
    owner_id = str(credentials['ownerid'][0])
    _log_games = str(credentials['loggames'][0])
    if _log_games == 'True':
        _log_games = True
    elif _log_games == 'False':
        _log_games = False
    _is_official_bot = str(credentials['Is_Official_Bot_Account'][0])
    _pm_commands_list = str(credentials['PM_Commands'][0])
    _bot_prefix = str(credentials['bot_prefix'][0])
    if _pm_commands_list == 'True':
        _pm_commands_list = True
    elif _pm_commands_list == 'False':
        _pm_commands_list = False

if _log_games:
    # noinspection PyUnresolvedReferences
    import BotLogs
    DBLogs = BotLogs.BotLogs()


# noinspection PyUnusedLocal,PyPep8Naming
class bot_data:
    """
        This class is for Internal use only!!!
    """
    def __init__(self):
        pass

    @asyncio.coroutine
    def attack_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.content.startswith(_bot_prefix + 'attack'):
            if message.author.id in banlist['Users']:
                return
            else:
                for user in message.mentions:
                    yield from client.send_message(user, str(botmessages['attack_command_data'][0]))
                    break
                else:
                    yield from client.send_message(message.author, str(botmessages['attack_command_data'][1]))

    @asyncio.coroutine
    def randomcoin_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.content.startswith(_bot_prefix + 'coin'):
            if message.author.id in banlist['Users']:
                return
            else:
                msg = random.randint(0, 1)
                if msg == 0:
                    heads_coin = "{0}{1}resources{1}images{1}coins{1}Heads.png".format(sys.path[0], sepa)
                    try:
                        yield from client.send_file(message.channel, heads_coin)
                    except discord.errors.Forbidden:
                        try:
                            message_data = str(botmessages['coin_command_data'][0])
                            yield from client.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                if msg == 1:
                    tails_coin = "{0}{1}resources{1}images{1}coins{1}Tails.png".format(sys.path[0], sepa)
                    try:
                        yield from client.send_file(message.channel, tails_coin)
                    except discord.errors.Forbidden:
                        try:
                            message_data = str(botmessages['coin_command_data'][0])
                            yield from client.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def colors_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.content.startswith(_bot_prefix + 'color'):
            if message.author.id in banlist['Users']:
                return
            else:
                if _bot_prefix + "pink" in message.content:
                    desrole = message.content[len(_bot_prefix + "color " + _bot_prefix + "pink "):].strip()
                    role = discord.utils.find(lambda role: role.name == desrole, message.channel.server.roles)
                    try:
                        yield from client.edit_role(message.channel.server, role, color=discord.Colour(int(
                            'ff3054', 16)))
                    except discord.errors.Forbidden:
                        try:
                            message_data = str(botmessages['color_command_data'][0])
                            yield from client.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.errors.HTTPException:
                        return
                    except AttributeError:
                        return
                if _bot_prefix + "brown" in message.content:
                    desrole = message.content[len(_bot_prefix + "color " + _bot_prefix + "brown "):].strip()
                    role = discord.utils.find(lambda role: role.name == desrole, message.channel.server.roles)
                    try:
                        yield from client.edit_role(message.channel.server, role, color=discord.Colour(int(
                            '652d2d', 16)))
                    except discord.errors.Forbidden:
                        try:
                            message_data = str(botmessages['color_command_data'][0])
                            yield from client.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.errors.HTTPException:
                        return
                    except AttributeError:
                        return

    @asyncio.coroutine
    def debug_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.content.startswith(_bot_prefix + 'eval'):
            if message.author.id == owner_id:
                debugcode = message.content[len(_bot_prefix + "eval "):].strip()
                if debugcode.rfind('yield from client.send_message(message.channel, ') is not -1:
                    debugcode = debugcode[len("yield from client.send_message(message.channel, "):].strip()
                    debugcode = debugcode.strip(")")
                    if debugcode.find("'") is not -1:
                        debugcode = debugcode.strip("'")
                    elif debugcode.find('"') is not -1:
                        debugcode = debugcode.strip('"')
                    if debugcode.find('message.author.mention') is not -1:
                        debugcode = debugcode.replace('message.author.mention + "', message.author.mention)
                    yield from client.send_message(message.channel, debugcode)
                else:
                    botowner = discord.utils.find(lambda member: member.id == owner_id,
                                                  message.channel.server.members)
                    try:
                        try:
                            debugcode = eval(debugcode)
                        except SystemExit:
                            pass
                        debugcode = "```py\n" + str(debugcode) + "\n```"
                        try:
                            yield from client.send_message(message.channel, debugcode)
                        except discord.errors.Forbidden:
                            msgdata = str(botmessages['eval_command_data'][0])
                            message_data = msgdata.format(message.channel.server.name, message.channel.name)
                            yield from client.send_message(botowner, message_data)
                            yield from client.send_message(botowner, debugcode)
                        except discord.errors.HTTPException:
                            if len(debugcode) > 2000:
                                result_info = str(botmessages['eval_command_data'][1])
                                yield from client.send_message(message.channel, result_info)
                    except Exception as e:
                        debugcode = traceback.format_exc()
                        debugcode = str(debugcode)
                        try:
                            yield from client.send_message(message.channel, "```py\n" + debugcode + "\n```")
                        except discord.errors.Forbidden:
                            msgdata = str(botmessages['eval_command_data'][0])
                            message_data = msgdata.format(message.channel.server.name, message.channel.name)
                            yield from client.send_message(botowner, message_data)
                            yield from client.send_message(botowner, "```py\n" + debugcode + "\n```")
            else:
                try:
                    result_info = str(botmessages['eval_command_data'][2])
                    yield from client.send_message(message.channel, result_info)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'debug'):
            # makes the owner AKA Creator of the bot only able to use this as this can be dangerous.
            if message.author.id == owner_id:
                debugcode_new = "# coding=utf-8\n" + message.content[len(_bot_prefix + "debug "):].strip()
                BotOwner = discord.utils.find(lambda member: member.id == owner_id, message.channel.server.members)
                try:
                    evalcodefile = '{0}{1}resources{1}exec_files{1}exec_temp.py'.format(sys.path[0], sepa)
                    eval_temp_code = io.open(evalcodefile, 'w+', encoding='utf-8')
                    debugcode_new += '\n'
                    eval_temp_code.write(debugcode_new)
                    eval_temp_code.close()
                    execoutputfile = '{0}{1}resources{1}exec_files{1}exec_output_temp.txt'.format(sys.path[0], sepa)
                    eval_temp_result_output = io.open(execoutputfile, 'w', encoding='utf-8')
                    out = eval_temp_result_output
                    p = subprocess.Popen("{0}{1}python {2}".format(sys.path[4], sepa, evalcodefile), stdout=out,
                                         stderr=out, shell=True)
                    p.wait()
                    eval_temp_result_output.close()
                    eval_temp_result_read = io.open(execoutputfile, encoding='utf-8')
                    eval_result = eval_temp_result_read.read()
                    if eval_result is not '':
                        debugcode = eval_result
                    else:
                        debugcode = 'None'
                    eval_temp_result_read.close()
                    try:
                        yield from client.send_message(message.channel, "```py\n" + debugcode + "\n```")
                    except discord.errors.Forbidden:
                        msgdata = str(botmessages['eval_command_data'][0])
                        message_data = msgdata.format(message.channel.server.name, message.channel.name)
                        yield from client.send_message(BotOwner, message_data)
                        yield from client.send_message(BotOwner, "```py\n" + debugcode + "\n```")
                    except discord.errors.HTTPException:
                        if len(debugcode) > 2000:
                            result_info = str(botmessages['eval_command_data'][1])
                            yield from client.send_message(message.channel, result_info)
                except Exception as e:
                    debugcode = traceback.format_exc()
                    debugcode = str(debugcode)
                    try:
                        yield from client.send_message(message.channel, "```py\n" + debugcode + "\n```")
                    except discord.errors.Forbidden:
                        msgdata = str(botmessages['eval_command_data'][0])
                        message_data = msgdata.format(message.channel.server.name, message.channel.name)
                        yield from client.send_message(BotOwner, message_data)
                        yield from client.send_message(BotOwner, "```py\n" + debugcode + "\n```")
            else:
                try:
                    result_info = str(botmessages['debug_command_data'][0])
                    yield from client.send_message(message.channel, result_info)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def games_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
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
                            DBLogs.gamelog(client, message, desgame)
                        yield from client.change_status(game=discord.Game(name=desgame, type=desgametype,
                                                                          url=stream_url))
                        try:
                            msgdata = str(botmessages['game_command_data'][0]).format(desgame)
                            message_data = msgdata.replace("idle", "streaming")
                            yield from client.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    else:
                        if _log_games == 'True':
                            DBLogs.gamelog(client, message, desgame)
                        yield from client.change_status(game=discord.Game(name=desgame), idle=True)
                        try:
                            msgdata = str(botmessages['game_command_data'][0]).format(desgame)
                            message_data = msgdata
                            yield from client.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'remgame'):
            if message.author.id in banlist['Users']:
                return
            else:
                game_name = str(consoletext['On_Ready_Game'][0])
                stream_url = "https://twitch.tv/decoraterbot"
                yield from client.change_status(game=discord.Game(name=game_name, type=1, url=stream_url))
                try:
                    yield from client.send_message(message.channel, str(botmessages['remgame_command_data'][0]))
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def invite_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.content.startswith(_bot_prefix + 'join'):
            if message.author.id in banlist['Users']:
                return
            else:
                if _is_official_bot == 'True':
                    yield from client.send_message(message.channel, str(botmessages['join_command_data'][3]))
                else:
                    code = message.content[len(_bot_prefix + "join "):].strip()
                    if code == '':
                        url = None
                    else:
                        url = code
                    if url is not None:
                        try:
                            yield from client.accept_invite(url)
                            msg_data = str(botmessages['join_command_data'][0])
                            yield from client.send_message(message.channel, msg_data)
                        except discord.errors.NotFound:
                            msg_data = str(botmessages['join_command_data'][1])
                            yield from client.send_message(message.channel, msg_data)
                    else:
                        yield from client.send_message(message.channel, str(botmessages['join_command_data'][2]))

    @asyncio.coroutine
    def kills_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.content.startswith(_bot_prefix + 'kill'):
            if message.author.id in banlist['Users']:
                return
            else:
                data = message.content[len(_bot_prefix + "kill "):].strip()
                if message.channel.is_private is not False:
                    msg = random.randint(1, 4)
                    if msg == 1:
                        message_data = str(botmessages['kill_command_data'][0]).format(message.author)
                        yield from client.send_message(message.channel, message_data)
                    if msg == 2:
                        message_data = str(botmessages['kill_command_data'][1]).format(message.author)
                        yield from client.send_message(message.channel, message_data)
                    if msg == 3:
                        message_data = str(botmessages['kill_command_data'][2]).format(message.author)
                        yield from client.send_message(message.channel, message_data)
                    if msg == 4:
                        message_data = str(botmessages['kill_command_data'][3]).format(message.author)
                        yield from client.send_message(message.channel, message_data)
                else:
                    if data.rfind(client.user.name) != -1:
                        try:
                            msg_data = str(botmessages['kill_command_data'][4])
                            yield from client.send_message(message.channel, msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    else:
                        msg = random.randint(1, 4)
                        for disuser in message.mentions:
                            if message.author == disuser:
                                try:
                                    msg_data = str(botmessages['kill_command_data'][4])
                                    yield from client.send_message(message.channel, msg_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                                break
                            if client.user == disuser:
                                try:
                                    msg_data = str(botmessages['kill_command_data'][4])
                                    yield from client.send_message(message.channel, msg_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                                break
                            user = discord.utils.find(lambda member: member.name == disuser.name,
                                                      message.channel.server.members)
                            if msg == 1:
                                try:
                                    msgdata = str(botmessages['kill_command_data'][5]).format(message.author, user)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                                break
                            if msg == 2:
                                try:
                                    msgdata = str(botmessages['kill_command_data'][6]).format(message.author, user)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                                break
                            if msg == 3:
                                try:
                                    msgdata = str(botmessages['kill_command_data'][7]).format(message.author, user)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                                break
                            if msg == 4:
                                try:
                                    msgdata = str(botmessages['kill_command_data'][8]).format(message.author, user)
                                    message_data = msgdata
                                    yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                                break
                        else:
                            if msg == 1:
                                try:
                                    message_data = str(botmessages['kill_command_data'][0]).format(message.author)
                                    yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                            if msg == 2:
                                try:
                                    message_data = str(botmessages['kill_command_data'][1]).format(message.author)
                                    yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                            if msg == 3:
                                try:
                                    message_data = str(botmessages['kill_command_data'][2]).format(message.author)
                                    yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                            if msg == 4:
                                try:
                                    message_data = str(botmessages['kill_command_data'][3]).format(message.author)
                                    yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def bot_mentioned_helper(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.author.id in banlist['Users']:
            return
        elif message.author.bot is True:
            return
        else:
            pref = _bot_prefix
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
                elif message.author.id == client.user.id:
                    return
                elif message.channel.server.id == "110373943822540800":
                    if message.author.id == "103607047383166976":
                        return
                    else:
                        info = str(botmessages['On_Bot_Mention_Message_Data'][0]).format(message.author)
                        yield from client.send_message(message.channel, info)
                elif message.channel.server.id == '101596364479135744':
                    if message.author.id == "110368240768679936":
                        return
                    else:
                        info = str(botmessages['On_Bot_Mention_Message_Data'][0]).format(message.author)
                        yield from client.send_message(message.channel, info)
                else:
                    info = str(botmessages['On_Bot_Mention_Message_Data'][0]).format(message.author)
                    try:
                        yield from client.send_message(message.channel, info)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def mention_ban_helper(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.author.id == client.user.id:
            return
        if message.channel.server.id == "105010597954871296":
            return
        if message.author.id == owner_id:
            return
        else:
            try:
                yield from client.ban(message.author)
                try:
                    message_data = str(botmessages['mention_spam_ban'][0]).format(message.author)
                    yield from client.send_message(message.channel, message_data)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)
            except discord.errors.Forbidden:
                try:
                    msgdata = str(botmessages['mention_spam_ban'][1]).format(message.author)
                    message_data = msgdata
                    yield from client.send_message(message.channel, message_data)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)
            except discord.HTTPException:
                try:
                    msgdata = str(botmessages['mention_spam_ban'][2]).format(message.author)
                    message_data = msgdata
                    yield from client.send_message(message.channel, message_data)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def mod_commands_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if len(message.mentions) > 5:
            yield from self.mention_ban_helper(client, message)
        if message.content.startswith(_bot_prefix + "ban"):
            if message.author.id == message.channel.server.owner.id or owner_id:
                for disuser in message.mentions:
                    listdata = message.channel.server.members
                    member = discord.utils.find(lambda member: member.name == disuser.name, listdata)
                    try:
                        yield from client.ban(member, delete_message_days=7)
                        try:
                            message_data = str(botmessages['ban_command_data'][0]).format(member)
                            yield from client.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.Forbidden:
                        try:
                            yield from client.send_message(message.channel, str(botmessages['ban_command_data'][1]))
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.HTTPException:
                        try:
                            yield from client.send_message(message.channel, str(botmessages['ban_command_data'][2]))
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    break
                else:
                    try:
                        yield from client.send_message(message.channel, str(botmessages['ban_command_data'][3]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
            else:
                try:
                    yield from client.send_message(message.channel, str(botmessages['ban_command_data'][4]))
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + "softban"):
            if message.author.id == message.channel.server.owner.id or owner_id:
                for disuser in message.mentions:
                    memberlist = message.channel.server.members
                    member = discord.utils.find(lambda member: member.name == disuser.name, memberlist)
                    try:
                        yield from client.ban(member, delete_message_days=7)
                        yield from client.unban(member.server, member)
                        try:
                            message_data = str(botmessages['softban_command_data'][0]).format(member)
                            yield from client.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.Forbidden:
                        try:
                            msg_data = str(botmessages['softban_command_data'][1])
                            yield from client.send_message(message.channel, msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.HTTPException:
                        try:
                            msg_data = str(botmessages['softban_command_data'][2])
                            yield from client.send_message(message.channel, msg_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    break
                else:
                    try:
                        yield from client.send_message(message.channel, str(botmessages['softban_command_data'][3]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
            else:
                try:
                    yield from client.send_message(message.channel, str(botmessages['softban_command_data'][4]))
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + "kick"):
            if message.author.id == message.channel.server.owner.id or owner_id:
                for disuser in message.mentions:
                    memberlist = message.channel.server.members
                    member = discord.utils.find(lambda member: member.name == disuser.name, memberlist)
                    try:
                        yield from client.kick(member)
                        try:
                            message_data = str(botmessages['kick_command_data'][0]).format(member)
                            yield from client.send_message(message.channel, message_data)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.Forbidden:
                        try:
                            yield from client.send_message(message.channel, str(
                                botmessages['kick_command_data'][1]))
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.HTTPException:
                        try:
                            yield from client.send_message(message.channel, str(
                                botmessages['kick_command_data'][2]))
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    break
                else:
                    try:
                        yield from client.send_message(message.channel, str(botmessages['kick_command_data'][3]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
            else:
                try:
                    yield from client.send_message(message.channel, str(botmessages['kick_command_data'][4]))
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def other_commands_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.content.startswith(_bot_prefix + 'commands'):
            if message.author.id in banlist['Users']:
                return
            else:
                if message.channel.is_private is not False:
                    if disabletinyurl is True:
                        yield from client.send_message(message.channel, botcommandsPM)
                    else:
                        yield from client.send_message(message.channel, botcommandsPMwithtinyurl)
                else:
                    if disabletinyurl is True:
                        try:
                            if _pm_commands_list is True:
                                yield from client.send_message(message.author, botcommands)
                            else:
                                yield from client.send_message(message.channel, botcommands)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    else:
                        try:
                            if _pm_commands_list is True:
                                yield from client.send_message(message.author, botcommandswithtinyurl)
                                msgdata = str(botmessages['commands_command_data'][6])
                                message_data = msgdata.format(message.author.mention)
                                try:
                                    yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                            else:
                                yield from client.send_message(message.channel, botcommandswithtinyurl)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'changelog'):
            if message.author.id in banlist['Users']:
                return
            else:
                try:
                    yield from client.send_message(message.channel, changelog.format(version + rev))
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'raid'):
            if message.author.id in banlist['Users']:
                return
            else:
                if message.channel.is_private is not False:
                    return
                else:
                    result = message.content.replace("::raid", "")
                    if result.startswith(" "):
                        result = result[len(" "):].strip()
                    try:
                        message_data = str(botmessages['raid_command_data'][0]).format(result)
                        yield from client.send_message(message.channel, message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'update'):
            if message.author.id in banlist['Users']:
                return
            else:
                if message.channel.is_private is not False:
                    return
                else:
                    try:
                        yield from client.send_message(message.channel,
                                                       str(botmessages['update_command_data'][0]).format(info))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'Libs'):
            if message.author.id in banlist['Users']:
                return
            else:
                libs = str(botmessages['Libs_command_data'][0])
                try:
                    yield from client.send_message(message.channel, libs)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'source'):
            if message.author.id in banlist['Users']:
                return
            else:
                try:
                    msgdata = sourcelink.format(message.author)
                    message_data = msgdata
                    yield from client.send_message(message.channel, message_data)
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'type'):
            if message.author.id in banlist['Users']:
                return
            else:
                yield from client.send_typing(message.channel)
        if message.content.startswith(_bot_prefix + 'pyversion'):
            if message.author.id in banlist['Users']:
                return
            else:
                if message.channel.is_private is not False:
                    return
                else:
                    python_platform = None
                    if bits == 8:
                        python_platform = "64-Bit"
                    elif bits == 4:
                        python_platform = "32-Bit"
                    vers = "```py\nPython v{0} {1}```".format(platform.python_version(), python_platform)
                    try:
                        yield from client.send_message(message.channel, vers)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'AgarScrub'):
            try:
                reply = 'https://imgflip.com/i/12yq2n'
                yield from client.send_message(message.channel, reply)
            except discord.errors.Forbidden:
                yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'stats'):
            server_count = str(len(client.servers))
            member_count = str(len(set([member for member in client.get_all_members()])))
            textchannels_count = str(len(set(
                [channel for channel in client.get_all_channels() if channel.type == discord.ChannelType.text])))
            formatted_data = str(
                botmessages['stats_command_data'][0]).format(server_count, member_count, textchannels_count)
            yield from client.send_message(message.channel, formatted_data)
        if message.content.startswith(_bot_prefix + 'rs'):
            filename1 = '{0}{1}resources{1}images{1}elsword{1}RS.jpg'.format(sys.path[0], sepa)
            file_object = open(filename1, 'rb')
            file_data = None
            if file_object is not None:
                file_data = file_object.read()
                file_object.close()
            yield from client.edit_profile(avatar=file_data)
        if message.content.startswith(_bot_prefix + 'as'):
            filename2 = '{0}{1}resources{1}images{1}elsword{1}AS.jpg'.format(sys.path[0], sepa)
            file_object = open(filename2, 'rb')
            file_data = None
            if file_object is not None:
                file_data = file_object.read()
                file_object.close()
            yield from client.edit_profile(avatar=file_data)
        if message.content.startswith(_bot_prefix + 'ai'):
            filename3 = '{0}{1}resources{1}images{1}elsword{1}AI.jpg'.format(sys.path[0], sepa)
            file_object = open(filename3, 'rb')
            file_data = None
            if file_object is not None:
                file_data = file_object.read()
                file_object.close()
            yield from client.edit_profile(avatar=file_data)
        if message.content.startswith(_bot_prefix + 'lk'):
            filename4 = '{0}{1}resources{1}images{1}elsword{1}LK.jpg'.format(sys.path[0], sepa)
            file_object = open(filename4, 'rb')
            file_data = None
            if file_object is not None:
                file_data = file_object.read()
                file_object.close()
            yield from client.edit_profile(avatar=file_data)
        if message.content.startswith(_bot_prefix + 'vp'):
            filename5 = '{0}{1}resources{1}images{1}elsword{1}VP.jpg'.format(sys.path[0], sepa)
            file_object = open(filename5, 'rb')
            file_data = None
            if file_object is not None:
                file_data = file_object.read()
                file_object.close()
            yield from client.edit_profile(avatar=file_data)
        if message.content.startswith(_bot_prefix + 'ws'):
            filename6 = '{0}{1}resources{1}images{1}elsword{1}WS.jpg'.format(sys.path[0], sepa)
            file_object = open(filename6, 'rb')
            file_data = None
            if file_object is not None:
                file_data = file_object.read()
                file_object.close()
            yield from client.edit_profile(avatar=file_data)
        if message.content.startswith(_bot_prefix + 'meme'):
            desdata = message.content[len(_bot_prefix + 'meme'):].strip()
            meme_error = False
            desdata = str(desdata)
            toptext = None
            bottext = None
            pic = None
            msg_mention_list_len = len(message.mentions) - 1
            if msg_mention_list_len == -1:
                msg_mention_list_len = 0
            if msg_mention_list_len > 0:
                if desdata.startswith(message.mentions[msg_mention_list_len].mention):
                    desdata = desdata.replace(" | ", "\n").replace('-', '--').replace(' ', '-')
                    desdata = desdata.splitlines()
                    try:
                        pic = message.mentions[msg_mention_list_len].avatar_url
                    except IndexError:
                        meme_error = True
                        msgdata = str(botmessages['meme_command_data'][0])
                        yield from client.send_message(message.channel, msgdata)
                    if not meme_error:
                        try:
                            toptext = desdata[1].replace('_', '__').replace('?', '~q').replace(
                                '%', '~p').replace('#', '~h').replace('/', '~s')
                            for x in message.mentions:
                                toptext = toptext.replace(x.mention, x.name)
                            toptext = toptext.replace('<', '').replace('>', '').replace('@', '')
                        except IndexError:
                            meme_error = True
                            msgdata = str(botmessages['meme_command_data'][1])
                            yield from client.send_message(message.channel, msgdata)
                    if not meme_error:
                        try:
                            bottext = desdata[2].replace('_', '__').replace(
                                '?', '~q').replace('%', '~p').replace('#', '~h').replace('/', '~s')
                            for x in message.mentions:
                                bottext = bottext.replace(x.mention, x.name)
                            bottext = bottext.replace('<', '').replace('>', '').replace('@', '')
                        except IndexError:
                            meme_error = True
                            msgdata = str(botmessages['meme_command_data'][2])
                            yield from client.send_message(message.channel, msgdata)
                    if not meme_error:
                        rep = "http://memegen.link/custom/{0}/{1}.jpg?alt={2}".format(toptext, bottext, pic)
                        yield from client.send_message(message.channel, rep)
            else:
                desdata = desdata.replace(" | ", "\n").replace('-', '--').replace(' ', '-')
                desdata = desdata.splitlines()
                try:
                    pic = str(desdata[0])
                except IndexError:
                    meme_error = True
                    msgdata = str(botmessages['meme_command_data'][0])
                    yield from client.send_message(message.channel, msgdata)
                if not meme_error:
                    try:
                        toptext = desdata[1].replace('_', '__').replace('?', '~q').replace(
                            '%', '~p').replace('#', '~h').replace('/', '~s')
                        for x in message.mentions:
                            toptext = toptext.replace(x.mention, x.name)
                        toptext = toptext.replace('<', '').replace('>', '').replace('@', '')
                    except IndexError:
                        meme_error = True
                        msgdata = str(botmessages['meme_command_data'][1])
                        yield from client.send_message(message.channel, msgdata)
                if not meme_error:
                    try:
                        bottext = desdata[2].replace('_', '__').replace('?', '~q').replace(
                            '%', '~p').replace('#', '~h').replace('/', '~s')
                        for x in message.mentions:
                            bottext = bottext.replace(x.mention, x.name)
                        bottext = bottext.replace('<', '').replace('>', '').replace('@', '')
                    except IndexError:
                        meme_error = True
                        msgdata = str(botmessages['meme_command_data'][2])
                        yield from client.send_message(message.channel, msgdata)
                if not meme_error:
                    rep = "http://memegen.link/{0}/{1}/{2}.jpg".format(pic, toptext, bottext)
                    yield from client.send_message(message.channel, rep)
        if message.content.startswith(_bot_prefix + 'givecreds'):
            """
                This command tricks a bot to giving the owner of this bot 200 credits.
            """
            ownermentiondata = '<@' + owner_id + '>'
            yield from client.send_message(message.channel, 't!daily {0}'.format(ownermentiondata))
        """
            This below is left in so anyone could have a example of itterating through roles to find the right one
            that they want.

            Note: This uses the json module to load up ppl who was listed in a json file that cannot use the bot.

            This does also only send 1 message after it gets the entire role list consisting of the role name
            and it's id.

            if message.content.startswith(_bot_prefix + 'roleinfo'):
                roleinfo = None
                if message.author.id in banlist['Users']:
                    message_data = " Due to Continuous abuse you have been Bot Banned."
                    yield from client.send_message(message.channel, message.author.mention + message_data)
                else:
                    for role in message.channel.server.roles:
                        if roleinfo is None:
                            roleinfo = "role name: {0}, role id: {1}\n".format(role.name, role.id)
                        else:
                            roleinfo += "role name: {0}, role id: {1}\n".format(role.name, role.id)
                    yield from client.send_message(message.channel, "```" + roleinfo + "```")
            """

    if PY35 or PY36:
        # noinspection PyMethodMayBeStatic
        async def prune_command_iterater_helper(self, client, message, num, sent_prune_error_message):
            """
            Prunes Messages.
            :param self:
            :param client: Discord Client.
            :param message: Message
            :param num:
            :param sent_prune_error_message: Bool
            :return: Nothing.
            """
            try:
                await client.purge_from(message.channel, limit=num + 1)
            except discord.HTTPException:
                if sent_prune_error_message is False:
                    sent_prune_error_message = True
                    await client.send_message(message.channel, str(botmessages['prune_command_data'][0]))
                else:
                    return

        # noinspection PyMethodMayBeStatic
        async def clear_command_iterater_helper(self, client, message):
            """
            Clears the bot's messages.
            :param self:
            :param client: Discord Client.
            :param message: Message.
            :return: Nothing.
            """
            def botauthor(m):
                return m.author == client.user

            try:
                await client.purge_from(message.channel, limit=100, check=botauthor)
            except discord.HTTPException:
                return
    else:
        # noinspection PyTypeChecker
        @asyncio.coroutine
        def prune_command_iterater_helper(self, client, message, num, sent_prune_error_message):
            """
            Prunes Messages.
            :param self:
            :param client: Discord Client.
            :param message: Message
            :param num:
            :param sent_prune_error_message: Bool
            :return: Nothing.
            """
            try:
                yield from client.purge_from(message.channel, limit=num + 1)
            except discord.HTTPException:
                if sent_prune_error_message is False:
                    sent_prune_error_message = True
                    yield from client.send_message(message.channel, str(botmessages['prune_command_data'][0]))
                else:
                    return

        # noinspection PyTypeChecker
        @asyncio.coroutine
        def clear_command_iterater_helper(self, client, message):
            """
            Clears the bot's messages.
            :param self:
            :param client: Discord Client.
            :param message: Message.
            :return: Nothing.
            """
            def botauthor(m):
                return m.author == client.user

            try:
                yield from client.purge_from(message.channel, limit=100, check=botauthor)
            except discord.HTTPException:
                return

    @asyncio.coroutine
    def prune_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        global sent_prune_error_message
        if message.content.startswith(_bot_prefix + 'prune'):
            if message.author.id in banlist['Users']:
                return
            else:
                sent_prune_error_message = False
                role = discord.utils.find(lambda role: role.name == 'Bot Commander', message.channel.server.roles)
                """
                if message.author.id == owner_id:
                    opt = message.content[len(_bot_prefix + "prune "):].strip()
                    num = 1
                    if opt:
                        try:
                            num = int(opt)
                        except:
                            return
                    yield from self.prune_command_iterater_helper(client, message, num, sent_prune_error_message)
                else:
                """
                if role in message.author.roles:
                    opt = message.content[len(_bot_prefix + "prune "):].strip()
                    num = 1
                    if opt:
                        try:
                            num = int(opt)
                        except Exception as e:
                            return
                    yield from self.prune_command_iterater_helper(client, message, num, sent_prune_error_message)
                else:
                    try:
                        yield from client.send_message(message.channel, str(botmessages['prune_command_data'][1]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)

    # Unused but too lazy to remove this.

    @asyncio.coroutine
    def bot_roles_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.content.startswith(_bot_prefix + 'giveme'):
            if message.channel.server and message.channel.server.id == "81812480254291968":
                desrole = message.content[len(_bot_prefix + "giveme "):].strip()
                role = discord.utils.find(lambda role: role.name == 'Muted', message.channel.server.roles)
                role3 = discord.utils.find(lambda role: role.name == 'Students', message.channel.server.roles)
                if 'admin' in desrole:
                    if 'Muted' in message.author.roles:
                        yield from client.add_roles(message.author, role)
                        yield from client.send_message(message.channel, str(botmessages['giveme_command_data'][0]))
                    else:
                        yield from client.send_message(message.channel, str(botmessages['giveme_command_data'][5]))
                elif 'student' in desrole:
                    if 'Students' in message.author.roles:
                        yield from client.add_roles(message.author, role3)
                        yield from client.send_message(message.channel, str(botmessages['giveme_command_data'][1]))
                    else:
                        yield from client.send_message(message.channel, str(botmessages['giveme_command_data'][6]))
            else:
                if message.channel.server and message.channel.server.id == "127233852182626304":
                    desrole = message.content[len(_bot_prefix + "giveme "):].strip()
                    rolelist = message.channel.server.roles
                    role = discord.utils.find(lambda role: role.name == '3rd Party Developer', rolelist)
                    role3 = discord.utils.find(lambda role: role.name == 'Streamer', rolelist)
                    if 'dev' in desrole:
                        if role not in message.author.roles:
                            yield from client.add_roles(message.author, role)
                            yield from client.send_message(message.channel, str(
                                botmessages['giveme_command_data'][2]))
                        else:
                            yield from client.send_message(message.channel, str(
                                botmessages['giveme_command_data'][7]))
                    elif 'stream' in desrole:
                        if role3 not in message.author.roles:
                            yield from client.add_roles(message.author, role3)
                            yield from client.send_message(message.channel, str(
                                botmessages['giveme_command_data'][3]))
                        else:
                            yield from client.send_message(message.channel, str(
                                botmessages['giveme_command_data'][8]))
                else:
                    try:
                        yield from client.send_message(message.channel, str(
                            botmessages['giveme_command_data'][4]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
        if message.content.startswith(_bot_prefix + 'remove'):
            if message.channel.server and message.channel.server.id == "127233852182626304":
                desrole = message.content[len(_bot_prefix + "remove "):].strip()
                rolelist = message.channel.server.roles
                role = discord.utils.find(lambda role: role.name == '3rd Party Developer', rolelist)
                role3 = discord.utils.find(lambda role: role.name == 'Streamer', rolelist)
                if 'dev' in desrole:
                    if role in message.author.roles:
                        yield from client.remove_roles(message.author, role)
                        yield from client.send_message(message.channel, str(botmessages['remove_command_data'][0]))
                    else:
                        yield from client.send_message(message.channel, str(botmessages['remove_command_data'][2]))
                elif 'stream' in desrole:
                    if role3 in message.author.roles:
                        yield from client.remove_roles(message.author, role3)
                        yield from client.send_message(message.channel, str(botmessages['remove_command_data'][1]))
                    else:
                        yield from client.send_message(message.channel, str(botmessages['remove_command_data'][3]))
            else:
                return

    @asyncio.coroutine
    def bot_say_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.content.startswith(_bot_prefix + 'say'):
            if message.author.id in banlist['Users']:
                return
            else:
                say = message.content[len(_bot_prefix + "say "):].strip()
                if say.rfind(_bot_prefix) != -1:
                    message_data = str(botmessages['say_command_data'][0]).format(message.author)
                    yield from client.send_message(message.channel, message_data)
                elif say.rfind("@") != -1:
                    message_data = str(botmessages['say_command_data'][1]).format(message.author)
                    yield from client.send_message(message.channel, message_data)
                else:
                    try:
                        yield from client.send_message(message.channel, say)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
                    except discord.errors.HTTPException:
                        return

    @asyncio.coroutine
    def more_commands_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if client.user.mention in message.content:
            yield from self.bot_mentioned_helper(client, message)
        elif message.content.startswith(_bot_prefix + "clear"):
            if message.author.id in banlist['Users']:
                return
            else:
                yield from self.clear_command_iterater_helper(client, message)
        elif message.content.startswith(_bot_prefix + 'botban'):
            if message.author.id == owner_id:
                if len(message.mentions) < 1:
                    try:
                        yield from client.send_message(message.channel, str(
                            botmessages['bot_ban_command_data'][2]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    if message.mentions[0].id not in banlist['Users']:
                        try:
                            banlist['Users'].append(message.mentions[0].id)
                            json.dump(banlist, open("{0}{1}resources{1}ConfigData{1}BotBanned.json".format(sys.path[0],
                                                                                                           sepa), "w"))
                            try:
                                message_data = str(
                                    botmessages['bot_ban_command_data'][0]).format(message.mentions[0])
                                yield from client.send_message(message.channel, message_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                            except Exception as e:
                                try:
                                    messagedata = str(
                                        botmessages['bot_ban_command_data'][1]).format(message.mentions[0])
                                    message_data = messagedata + str(botmessages['bot_ban_command_data'][2])
                                    yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError.resolve_send_message_error(client, message)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
        elif message.content.startswith(_bot_prefix + 'botunban'):
            if message.author.id == owner_id:
                if len(message.mentions) < 1:
                    try:
                        yield from client.send_message(message.channel, str(
                            botmessages['bot_unban_command_data'][2]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    if message.mentions[0].id in banlist['Users']:
                        try:
                            tobotunban = banlist['Users']
                            tobotunban.remove(message.mentions[0].id)
                            json.dump(banlist, open("{0}{1}resources{1}ConfigData{1}BotBanned.json".format(sys.path[0],
                                                                                                           sepa), "w"))
                            try:
                                message_data = str(
                                    botmessages['bot_unban_command_data'][0]).format(message.mentions[0])
                                yield from client.send_message(message.channel, message_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                        except Exception as e:
                            try:
                                messagedata = str(
                                    botmessages['bot_unban_command_data'][1]).format(message.mentions[0])
                                message_data = messagedata + str(botmessages['bot_unban_command_data'][2])
                                yield from client.send_message(message.channel, message_data)
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def userdata_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if message.content.startswith(_bot_prefix + "userinfo"):
            if message.author.id in banlist['Users']:
                return
            else:
                for disuser in message.mentions:
                    username = message.mentions[0].name
                    seenin = set(
                        [member.server.name for member in client.get_all_members() if member.name == username])
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
                        yield from client.send_message(message.channel, data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)
                    break
                else:
                    seenin = set(
                        [member.server.name for member in client.get_all_members()
                         if member.name == message.author.name])
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
                        yield from client.send_message(message.channel, data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def convert_url_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
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
                            yield from client.send_message(message.channel, result)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    else:
                        if url.startswith("https://"):
                            pass
                        elif url.startswith("ftp://"):
                            pass
                        else:
                            try:
                                yield from client.send_message(message.channel, str(
                                    botmessages['tinyurl_command_data'][1]))
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                    if url.startswith("https://"):
                        link = TinyURL.TinyURL.create_one(url)
                        link = str(link)
                        result = str(botmessages['tinyurl_command_data'][0]).format(link)
                        try:
                            yield from client.send_message(message.channel, result)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    else:
                        if url.startswith("ftp://"):
                            pass
                        elif url.startswith("http://"):
                            pass
                        else:
                            try:
                                yield from client.send_message(message.channel, str(
                                    botmessages['tinyurl_command_data'][1]))
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                    if url.startswith("ftp://"):
                        link = TinyURL.TinyURL.create_one(url)
                        link = str(link)
                        result = str(botmessages['tinyurl_command_data'][0]).format(link)
                        try:
                            yield from client.send_message(message.channel, result)
                        except discord.errors.Forbidden:
                            yield from BotPMError.resolve_send_message_error(client, message)
                    else:
                        if url.startswith("http://"):
                            pass
                        elif url.startswith("https://"):
                            pass
                        else:
                            try:
                                yield from client.send_message(message.channel, str(
                                    botmessages['tinyurl_command_data'][1]))
                            except discord.errors.Forbidden:
                                yield from BotPMError.resolve_send_message_error(client, message)
                else:
                    try:
                        yield from client.send_message(message.channel, str(botmessages['tinyurl_command_data'][2]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(client, message)

    @asyncio.coroutine
    def scan_for_invite_url_only_pm_code(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        if _is_official_bot == 'True':
            if message.content.startswith('https://discord.gg/'):
                yield from client.send_message(message.channel, str(botmessages['join_command_data'][3]))
            if message.content.startswith('http://discord.gg/'):
                yield from client.send_message(message.channel, str(botmessages['join_command_data'][3]))


class BotCommands:
    """
    Basic Messge Commands.
    """
    def __init__(self):
        self.bot = bot_data()

    @asyncio.coroutine
    def attack(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.attack_code(client, message)

    @asyncio.coroutine
    def randomcoin(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.randomcoin_code(client, message)

    @asyncio.coroutine
    def colors(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.colors_code(client, message)

    @asyncio.coroutine
    def debug(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.debug_code(client, message)

    @asyncio.coroutine
    def games(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.games_code(client, message)

    @asyncio.coroutine
    def invite(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.invite_code(client, message)

    @asyncio.coroutine
    def kills(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.kills_code(client, message)

    @asyncio.coroutine
    def mod_commands(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.mod_commands_code(client, message)

    @asyncio.coroutine
    def other_commands(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.other_commands_code(client, message)

    @asyncio.coroutine
    def prune(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.prune_code(client, message)

    @asyncio.coroutine
    def bot_roles(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.bot_roles_code(client, message)

    @asyncio.coroutine
    def bot_say(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.bot_say_code(client, message)

    @asyncio.coroutine
    def more_commands(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.more_commands_code(client, message)

    @asyncio.coroutine
    def userdata(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.userdata_code(client, message)

    @asyncio.coroutine
    def convert_url(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.convert_url_code(client, message)

    @asyncio.coroutine
    def scan_for_invite_url_only_pm(self, client, message):
        """
        Bot Commands.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.scan_for_invite_url_only_pm_code(client, message)
