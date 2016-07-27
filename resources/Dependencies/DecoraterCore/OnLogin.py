# coding=utf-8
import discord
from discord.__init__ import __version__
# noinspection PyPackageRequirements
from colorama import init
# noinspection PyPackageRequirements
from colorama import Fore, Back, Style
import asyncio

init()

async def on_login(client):
    print(Fore.GREEN + Style.BRIGHT + Back.BLACK + 'Logged in as ' + client.user.name)
    print("Bot id=" + client.user.id)
    print('Discord.py v' + __version__ + ' Async')
    print('-------------------------------')
    await client.change_status(game=discord.Game(name='on my Playstation 2.'), idle=False)
