# coding=utf-8
import os
import sys
try:
    import discord
except ImportError:
    appendpath = sys.path[0] + "\\resources\\Dependencies"
    sys.path.append(appendpath)
    import discord
import DecoraterBotCore
import os.path
import asyncio
import logging
import json
import io

PATH = sys.path[0] + '\\resources\\ConfigData\\Credentials.json'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    credsfile = io.open(PATH, 'r')
    credentials = json.load(credsfile)
    _discord_logger = str(credentials['discord_py_logger'][0])
    if _discord_logger == 'True':
        _discord_logger = True
    elif _discord_logger == 'False':
        _discord_logger = False

# noinspection PyUnboundLocalVariable
if _discord_logger is not False:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=sys.path[0] + '\\resources\\Logs\\discordpy.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

client = discord.Client()
DecoraterBotCore.Core.BotCore.changewindowtitle()
DecoraterBotCore.Core.BotCore.changewindowsize()


@client.event
async def on_message(message):
    # noinspection PyTypeChecker,PyCallByClass
    await DecoraterBotCore.Core.BotCore.commands(client, message)


@client.event
async def on_message_delete(message):
    # noinspection PyTypeChecker,PyCallByClass
    await DecoraterBotCore.Core.BotCore.deletemessage(client, message)


@client.event
async def on_message_edit(before, after):
    # noinspection PyTypeChecker,PyCallByClass
    await DecoraterBotCore.Core.BotCore.editmessage(client, before, after)


@client.event
async def on_member_ban(member):
    # noinspection PyTypeChecker,PyCallByClass
    await DecoraterBotCore.Core.BotCore.memberban(client, member)


@client.event
async def on_member_unban(server, user):
    await DecoraterBotCore.Core.BotCore.memberunban(server, user)


@client.event
async def on_member_remove(member):
    # noinspection PyTypeChecker,PyCallByClass
    await DecoraterBotCore.Core.BotCore.memberremove(client, member)


@client.event
async def on_member_join(member):
    # noinspection PyTypeChecker,PyCallByClass
    await DecoraterBotCore.Core.BotCore.memberjoin(client, member)


@client.event
async def on_ready():
    # noinspection PyTypeChecker,PyCallByClass
    await DecoraterBotCore.Core.BotCore._bot_ready(client)

# noinspection PyTypeChecker,PyCallByClass
DecoraterBotCore.BotCore._login_helper(client)
