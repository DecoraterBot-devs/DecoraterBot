# coding=utf-8
"""
The MIT License (MIT)

Copyright (c) 2015-2016 AraHaan

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import discord
import asyncio
import os
import os.path
import aiohttp
import sys
import json
import io
from discord.__init__ import __version__
from colorama import init
from colorama import Fore, Back, Style

sepa = os.sep

init()

consoledatafile = io.open('{0}{1}resources{1}ConfigData{1}ConsoleWindow.json'.format(sys.path[0], sepa))
consoletext = json.load(consoledatafile)
consoledatafile.close()

botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.json'.format(sys.path[0], sepa))
botmessages = json.load(botmessagesdata)
botmessagesdata.close()

PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(sys.path[0], sepa)

global reconnects
reconnects = 0
global is_bot_logged_in
is_bot_logged_in = False


class bot_data:
    """
        This Class is for Internal Use only!!!
    """
    def __init__(self):
        pass

    def login_info_code(self, client):
        """
        Allows the bot to Connect / Reconnect.
        NOTE: Reconnection is not always 100% due to sometimes throwing a RuntimeError because of a Event loop getting
        closed in Discord.py. Sadly the run fucntion does not reopen/recreate that loop.
        :param client: Discord Client.
        :return: Nothing.
        """
        global is_bot_logged_in
        global reconnects
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            credsfile = io.open(PATH)
            credentials = json.load(credsfile)
            discord_user_email = str(credentials['email'][0])
            if discord_user_email == 'None':
                discord_user_email = None
            discord_user_password = str(credentials['password'][0])
            if discord_user_password == 'None':
                discord_user_password = None
            bot_token = str(credentials['token'][0])
            if is_bot_logged_in:
                is_bot_logged_in = False
            if bot_token == 'None':
                bot_token = None
            try:
                if discord_user_email and discord_user_password is not None:
                    client.run(discord_user_email, discord_user_password)
                elif bot_token is not None:
                    # This is for logging into the bot with a token.
                    client.run(bot_token)
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
            except discord.errors.UnknownConnectionError:
                print(str(consoletext['Unknown_Connection_Error'][0]))
                sys.exit(2)
            except TypeError:
                return
            except KeyboardInterrupt:
                return
            except asyncio.futures.InvalidStateError:
                reconnects += 1
                if reconnects != 0:
                    print('Bot is currently reconnecting for {0} times.'.format(str(reconnects)))
                    # sleeptime = reconnects * 5
                    # asyncio.sleep(sleeptime)
                    self.login_info_code(client)
            except aiohttp.errors.ClientOSError:
                reconnects += 1
                if reconnects != 0:
                    print('Bot is currently reconnecting for {0} times.'.format(str(reconnects)))
                    # sleeptime = reconnects * 5
                    # asyncio.sleep(sleeptime)
                    self.login_info_code(client)
            if is_bot_logged_in:
                if not client.is_logged_in:
                    pass
                else:
                    reconnects += 1
                    if reconnects != 0:
                        print('Bot is currently reconnecting for {0} times.'.format(str(reconnects)))
                        # sleeptime = reconnects * 5
                        # asyncio.sleep(sleeptime)
                        self.login_info_code(client)
        else:
            print(str(consoletext['Credentials_Not_Found'][0]))
            sys.exit(2)

    @asyncio.coroutine
    def on_login_code(self, client):
        """
        Function that does the on_ready event stuff after logging in.
        :param client: Discord Client.
        :return: Nothing.
        """
        global logged_in
        if logged_in:
            logged_in = False
            message_data = str(botmessages['On_Ready_Message'][0])
            try:
                yield from client.send_message(discord.Object(id='118098998744580098'), message_data)
            except discord.errors.Forbidden:
                return
            try:
                yield from client.send_message(discord.Object(id='103685935593435136'), message_data)
            except discord.errors.Forbidden:
                return
            bot_name = client.user.name
            print(Fore.GREEN + Back.BLACK + Style.BRIGHT + str(
                consoletext['Window_Login_Text'][0]).format(bot_name, client.user.id, __version__))
        if not logged_in:
            game_name = str(consoletext['On_Ready_Game'][0])
            stream_url = "https://twitch.tv/decoraterbot"
            yield from client.change_status(game=discord.Game(name=game_name, type=1, url=stream_url))

    @staticmethod
    def variable_code():
        """
        Function that makes Certain things on the on_ready event only happen 1 time only. (eg the logged in printing
        stuff)
        :return: Nothing.
        """
        global logged_in
        logged_in = True


class BotLogin:
    """
    Base Class for getting the bot login.
    """
    def __init__(self):
        self.bot = bot_data()

    def login_info(self, client):
        """
        Function for Gettign the bot online.
        :param client: Discord Client.
        :return: Nothing.
        """
        self.bot.login_info_code(client)

    @asyncio.coroutine
    def on_login(self, client):
        """
        Calls the Function that does the on_ready event stuff.
        :param client: Discord Client.
        :return: Nothing.
        """
        yield from self.bot.on_login_code(client)

    def variable(self):
        """
        For catching things and only making certain things on the ready event only done 1 time.
        :return: Nothing.
        """
        self.bot.variable_code()
