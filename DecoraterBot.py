#coding=utf-8
import os
import DecoraterBotCore
import sys
import os.path
import discord
import asyncio

client = discord.Client()
DecoraterBotCore.Core.changeWindowTitle()
DecoraterBotCore.Core.changeWindowSize()
DecoraterBotCore.OnLogin.variable()

@client.event
@asyncio.coroutine
def on_message(message):
    DecoraterBotCore.Core.commands(client, message)

DecoraterBotCore.Core.on_error(on_message)

@client.event
@asyncio.coroutine
def on_message_delete(message):
    DecoraterBotCore.Core.deletemessage(message)

@client.event
@asyncio.coroutine
def on_message_edit(before, after):
    DecoraterBotCore.Core.editmessage(before, after)

@client.event
@asyncio.coroutine
def on_channel_create(channel):
    DecoraterBotCore.Channels.data(client, channel)

@client.event
@asyncio.coroutine
def on_ready():
    DecoraterBotCore.OnLogin.on_login(client)

DecoraterBotCore.Logininfo.login_info(client)