# coding=utf-8
import os
import discord
# noinspection PyPackageRequirements
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
    sys.path.append(sys.path[0] + "\\Dependencies\\DecoraterBotCore")
    import Ignore
import Login
import BotCommands
import BotPMError

# for finding ffmpeg
bits = ctypes.sizeof(ctypes.c_voidp)
if bits == 4:
    os.chdir(sys.path[0] + "\\resources\\ffmpeg\\x86")
elif bits == 8:
    os.chdir(sys.path[0] + "\\resources\\ffmpeg\\x64")

jsonfile = io.open(sys.path[0] + '\ConfigData\BotBanned.json', 'r')
somedict = json.load(jsonfile)
consoledatafile = io.open(sys.path[0] + '\ConfigData\ConsoleWindow.json', 'r')
consoletext = json.load(consoledatafile)
botmessagesdata = io.open(sys.path[0] + '\ConfigData\BotMessages.json', 'r')
botmessages = json.load(botmessagesdata)

version = str(consoletext['WindowVersion'][0])
start = time.time()
Login.BotLogin.variable()

PATH = sys.path[0] + '\ConfigData\Credentials.json'

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
    def changewindowtitle():
        ctypes.windll.kernel32.SetConsoleTitleW(str(consoletext['WindowName'][0]) + version)

    def changewindowsize():
        # noinspection PyUnusedLocal
        cmd = "mode con: cols=80 lines=23"
    #    subprocess.Popen(cmd, shell=True)

    # noinspection PyUnboundLocalVariable,PyUnusedLocal
    async def commands(client, message):
        # noinspection PyTypeChecker,PyCallByClass
        await Ignore.BotIgnores.ignore(client, message)
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
                # noinspection PyPep8
                time_001 = str(botmessages['Uptime_command_data'][0]) + days + str(
                    botmessages['Uptime_command_data'][1])
                time_002 = hours + str(botmessages['Uptime_command_data'][2]) + minutes
                # noinspection PyPep8
                time_003 = str(botmessages['Uptime_command_data'][3]) + seconds + str(
                    botmessages['Uptime_command_data'][4])
                time_parse = time_001 + time_002 + time_003
                try:
                    await client.send_message(message.channel, time_parse)
                except discord.errors.Forbidden:
                    return
        if message.content.startswith(_bot_prefix + "hlreload"):
            if message.author.id == discord_user_id:
                desmod_new = message.content.lower()[len(_bot_prefix + 'hlreload '):].strip()
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
                        # noinspection PyUnboundLocalVariable
                        if desmod == 'Ignore':
                            try:
                                rsn = reload_reason
                                await BotCommands.BotCommands._reload_commands_bypass1(client, message, rsn)
                                module = sys.modules.get(desmod)
                                importlib.reload(module)
                                await BotCommands.BotCommands._reload_commands_bypass2(client, message)
                                try:
                                    msgdata = str(botmessages['reload_command_data'][0])
                                    message_data = msgdata + ' Reloaded ' + desmod + '.'
                                    if desmod == 'BotLogs':
                                        if rsn is not None:
                                            message_data = message_data + ' Reason: ' + rsn
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

    async def deletemessage(client, message):
        # noinspection PyTypeChecker,PyCallByClass
        await Ignore.BotEvents._resolve_delete_method(client, message)

    async def editmessage(client, before, after):
        # noinspection PyTypeChecker,PyCallByClass
        await Ignore.BotEvents._resolve_edit_method(client, before, after)

    async def memberban(client, member):
        # noinspection PyTypeChecker,PyCallByClass
        await Ignore.BotEvents._resolve_onban(client, member)

    async def memberunban(client, member):
        # noinspection PyTypeChecker,PyCallByClass
        await Ignore.BotEvents._resolve_onunban(client, member)

    async def memberremove(client, member):
        # noinspection PyTypeChecker,PyCallByClass
        await Ignore.BotEvents._resolve_onremove(client, member)

    async def memberjoin(client, member):
        # noinspection PyTypeChecker,PyCallByClass
        await Ignore.BotEvents._resolve_onjoin(client, member)

    def _login_helper(client):
        Login.BotLogin.login_info(client)

    async def _bot_ready(client):
        await Login.BotLogin.on_login(client)
        await Ignore.BotEvents._resolve_on_login_voice_channel_join(client)
