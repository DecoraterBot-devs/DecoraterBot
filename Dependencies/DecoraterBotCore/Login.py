# coding=utf-8
import discord
import asyncio
import os
import os.path
import sys
import json
import time
import io
from discord.__init__ import __version__
# noinspection PyPackageRequirements
from colorama import init
# noinspection PyPackageRequirements
from colorama import Fore, Back, Style

init()

consoledatafile = io.open(sys.path[0] + '\ConfigData\ConsoleWindow.json', 'r')
consoletext = json.load(consoledatafile)

PATH = sys.path[0] + '\ConfigData\Credentials.json'

global reconnects
# noinspection PyRedeclaration
reconnects = 0
global is_bot_logged_in
# noinspection PyRedeclaration
is_bot_logged_in = False


class BotLogin:
    def __init__(self, client):
        self.bot = client

    @classmethod
    def login_info(self, client):
        global reconnects
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            credsfile = io.open(PATH, 'r')
            credentials = json.load(credsfile)
            discord_user_email = str(credentials['email'][0])
            if discord_user_email == 'None':
                discord_user_email = None
            discord_user_password = str(credentials['password'][0])
            if discord_user_password == 'None':
                discord_user_password = None
            bot_token = str(credentials['token'][0])
            if bot_token == 'None':
                bot_token = None
            try:
                client.run(discord_user_email, discord_user_password, bot_token)
                is_bot_logged_in = True
            except discord.errors.GatewayNotFound:
                print(str(consoletext['Login_Gateway_No_Find'][0]))
                return
            except discord.errors.LoginFailure:
                print(str(consoletext['Login_Failure'][0]))
                sys.exit(2)
            except discord.errors.InvalidToken:
                print(str(consoletext['Invalid_Token'][0]))
                sys.exit(2)
            except TypeError:
                return
            except KeyboardInterrupt:
                return
            if is_bot_logged_in is True:
                if client.is_logged_in is not False:
                    # This means the bot is currently logged in.
                    # noinspection PyUnusedLocal
                    nothing = None
                else:
                    # it must not be so this means we have to recurse.
                    reconnects = reconnects + 1
                    if reconnects != 0:
                        print('Bot is currently reconnecting for ' + str(reconnects) + ' times.')
                        sleeptime = reconnects * 5
                        time.sleep(sleeptime)
                        login_info(client)
        else:
            print(str(consoletext['Credentials_Not_Found'][0]))
            sys.exit(2)

    @classmethod
    async def on_login(self, client):
        global logged_in
        if logged_in is True:
            logged_in = False
            botmessagesdata = io.open(sys.path[0] + '\ConfigData\BotMessages.json', 'r')
            botmessages = json.load(botmessagesdata)
            print(Fore.GREEN + Back.BLACK + Style.BRIGHT + str(consoletext['Window_Login_Text'][0]) + client.user.name)
            print(str(consoletext['Window_Login_Text'][1]) + client.user.id)
            print(str(consoletext['Window_Login_Text'][2]) + __version__ + str(consoletext['Window_Login_Text'][3]))
            try:
                await client.send_message(discord.Object(id='118098998744580098'),
                                          str(botmessages['On_Ready_Message'][0]))
            except discord.errors.Forbidden:
                return
            try:
                await client.send_message(discord.Object(id='103685935593435136'),
                                          str(botmessages['On_Ready_Message'][0]))
            except discord.errors.Forbidden:
                return
            game_name = str(consoletext['On_Ready_Game'][0])
            # stream_url = "https://twitch.tv/guscaplan"
            stream_url = "https://twitch.tv/decoraterbot"
            await client.change_status(game=discord.Game(name=game_name, type=1, url=stream_url))

    @classmethod
    def variable(self):
        global logged_in
        logged_in = True
