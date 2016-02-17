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
async def on_message(message):
    await DecoraterBotCore.Core.commands(client, message)

@client.event
async def on_message_delete(message):
    DecoraterBotCore.Core.deletemessage(message)

@client.event
async def on_message_edit(before, after):
    DecoraterBotCore.Core.editmessage(before, after)

#@client.event
#async def on_channel_create(channel):
#    await DecoraterBotCore.Channels.data(client, channel)

@client.event
async def on_ready():
    await DecoraterBotCore.OnLogin.on_login(client)

DecoraterBotCore.Logininfo.login_info(client)