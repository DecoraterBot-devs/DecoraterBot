#coding=utf-8
import os
import DecoraterBotCore
import sys
import os.path
import discord
import asyncio
#import subprocess

#cmd = ".\\Music\\DecoraterBot.exe"
#subprocess.Popen(cmd, shell=False)

client = discord.Client()
DecoraterBotCore.Core.changeWindowTitle()
DecoraterBotCore.Core.changeWindowSize()
DecoraterBotCore.OnLogin.variable()

@client.event
async def on_message(message):
    await DecoraterBotCore.Core.commands(client, message)

@client.event
async def on_message_delete(message):
    await DecoraterBotCore.Core.deletemessage(client, message)

@client.event
async def on_message_edit(before, after):
    await DecoraterBotCore.Core.editmessage(client, before, after)

#@client.event
#async def on_channel_create(channel):
#    await DecoraterBotCore.Channels.data(client, channel)

@client.event
async def on_member_ban(member):
    await DecoraterBotCore.Ban.onban(client, member)

@client.event
async def on_member_unban(server, user):
    await DecoraterBotCore.Ban.onunban(server, user)

@client.event
async def on_ready():
    await DecoraterBotCore.OnLogin.on_login(client)

DecoraterBotCore.Logininfo.login_info(client)