import os
import discord
import DecoraterCore
import sys
import os.path
import ctypes
import asyncio

PATH='.\login.ini'

client = discord.Client()
DecoraterCore.Core.changeWindowTitle()

#@client.event
#async def on_message(message):
#    await DecoraterCore.Core.commands(client, message)

@client.event
async def on_ready():
    await DecoraterCore.OnLogin.on_login(client)

DecoraterCore.Logininfo.login_info(client)