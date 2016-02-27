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

@client.event
async def on_message(message):
    DecoraterCore.Core.commands(client, message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.readfp(open(PATH))
    discord_user_email = config.get("login2", "email")
    discord_user_password = config.get("login2", "password")
    client.run(discord_user_email, discord_user_password)
else:
    discord_user_email = 'email'
    discord_user_password = 'password'
    client.run(discord_user_email, discord_user_password)