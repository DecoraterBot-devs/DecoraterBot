# coding=utf-8
import os
import DecoraterBotCore
import sys
import os.path
import discord
import asyncio
import logging
import json
import io

PATH = sys.path[0] + '\ConfigData\Credentials.json'
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
    handler = logging.FileHandler(filename=sys.path[0] + '\Logs\discordpy.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

client = discord.Client()
DecoraterBotCore.Core.changeWindowTitle()
DecoraterBotCore.Core.changeWindowSize()
DecoraterBotCore.Login.variable()


@client.event
async def on_message(message):
    await DecoraterBotCore.Core.commands(client, message)


@client.event
async def on_message_delete(message):
    await DecoraterBotCore.Core.deletemessage(client, message)


@client.event
async def on_message_edit(before, after):
    await DecoraterBotCore.Core.editmessage(client, before, after)


@client.event
async def on_member_ban(member):
    await DecoraterBotCore.Core.memberban(client, member)


@client.event
async def on_member_unban(server, user):
    await DecoraterBotCore.Core.memberunban(server, user)


@client.event
async def on_member_remove(member):
    await DecoraterBotCore.Core.memberremove(client, member)


@client.event
async def on_ready():
    await DecoraterBotCore.Login.on_login(client)

DecoraterBotCore.Login.login_info(client)
