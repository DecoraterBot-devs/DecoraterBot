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
    await DecoraterBotCore.Ignore._resolve_onban(client, member)

@client.event
async def on_member_unban(server, user):
    await DecoraterBotCore.Ignore._resolve_onunban(server, user)

@client.event
async def on_ready():
    await DecoraterBotCore.Login.on_login(client)

DecoraterBotCore.Login.login_info(client)