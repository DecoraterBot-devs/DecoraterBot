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
import ctypes
import io
from discord.__init__ import __version__
from colorama import init
from colorama import Fore, Back, Style
import BotConfigReader


class BotData:
    """
        This Class is for Internal Use only!!!
    """
    def __init__(self):
        self.sepa = os.sep
        self.bits = ctypes.sizeof(ctypes.c_voidp)
        self.platform = None
        if self.bits == 4:
            self.platform = 'x86'
        elif self.bits == 8:
            self.platform = 'x64'
        self.path = sys.path[0]
        if self.path.find('\\AppData\\Local\\Temp') != -1:
            self.path = sys.executable.strip(
                'DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(self.platform, sys.platform,
                                                                                       sys.implementation,
                                                                                       sys.version_info))
        init()
        self.consoledatafile = io.open('{0}{1}resources{1}ConfigData{1}ConsoleWindow.json'.format(self.path, self.sepa))
        self.consoletext = json.load(self.consoledatafile)
        self.consoledatafile.close()
        self.botmessagesdata = io.open('{0}{1}resources{1}ConfigData{1}BotMessages.json'.format(self.path, self.sepa))
        self.botmessages = json.load(self.botmessagesdata)
        self.botmessagesdata.close()
        self.PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(self.path, self.sepa)
        self.BotConfig = BotConfigReader.BotConfigVars()
        self.reconnects = 0
        self.is_bot_logged_in = False
        self.logged_in = False

    def login_info_code(self, client):
        """
        Allows the bot to Connect / Reconnect.
        NOTE: Reconnection is not always 100% due to sometimes throwing a RuntimeError because of a Event loop getting
        closed in Discord.py. Sadly the run fucntion does not reopen/recreate that loop.
        :param client: Discord Client.
        :return: Nothing.
        """
        try:
            if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
                discord_user_email = self.BotConfig.discord_user_email
                if discord_user_email == 'None':
                    discord_user_email = None
                discord_user_password = self.BotConfig.discord_user_password
                if discord_user_password == 'None':
                    discord_user_password = None
                bot_token = self.BotConfig.bot_token
                if bot_token == 'None':
                    bot_token = None
                if self.is_bot_logged_in:
                    self.is_bot_logged_in = False
                try:
                    if discord_user_email and discord_user_password is not None:
                        client.run(discord_user_email, discord_user_password)
                    elif bot_token is not None:
                        # This is for logging into the bot with a token.
                        client.run(bot_token)
                        self.is_bot_logged_in = True
                except discord.errors.GatewayNotFound:
                    print(str(self.consoletext['Login_Gateway_No_Find'][0]))
                    return
                except discord.errors.LoginFailure:
                    print(str(self.consoletext['Login_Failure'][0]))
                    sys.exit(2)
                except discord.errors.InvalidToken:
                    print(str(self.consoletext['Invalid_Token'][0]))
                    sys.exit(2)
                except discord.errors.UnknownConnectionError:
                    print(str(self.consoletext['Unknown_Connection_Error'][0]))
                    sys.exit(2)
                except TypeError:
                    return
                except KeyboardInterrupt:
                    return
                except asyncio.futures.InvalidStateError:
                    self.reconnects += 1
                    if self.reconnects != 0:
                        print('Bot is currently reconnecting for {0} times.'.format(str(self.reconnects)))
                        # sleeptime = reconnects * 5
                        # asyncio.sleep(sleeptime)
                        self.login_info_code(client)
                except aiohttp.errors.ClientOSError:
                    self.reconnects += 1
                    if self.reconnects != 0:
                        print('Bot is currently reconnecting for {0} times.'.format(str(self.reconnects)))
                        # sleeptime = reconnects * 5
                        # asyncio.sleep(sleeptime)
                        self.login_info_code(client)
                if self.is_bot_logged_in:
                    if not client.is_logged_in:
                        pass
                    else:
                        self.reconnects += 1
                        if self.reconnects != 0:
                            print('Bot is currently reconnecting for {0} times.'.format(str(self.reconnects)))
                            # sleeptime = reconnects * 5
                            # asyncio.sleep(sleeptime)
                            self.login_info_code(client)
            else:
                print(str(self.consoletext['Credentials_Not_Found'][0]))
                sys.exit(2)
        except Exception as e:
            str(e)  # To Bypass issues later as this is a dummy thing. (for now)
            print("This Bot has Crashed for some reason.")
            sys.exit(2)

    @asyncio.coroutine
    def on_login_code(self, client):
        """
        Function that does the on_ready event stuff after logging in.
        :param client: Discord Client.
        :return: Nothing.
        """
        if self.logged_in:
            self.logged_in = False
            message_data = str(self.botmessages['On_Ready_Message'][0])
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
                self.consoletext['Window_Login_Text'][0]).format(bot_name, client.user.id, __version__))
        if not self.logged_in:
            game_name = str(self.consoletext['On_Ready_Game'][0])
            stream_url = "https://twitch.tv/decoraterbot"
            yield from client.change_status(game=discord.Game(name=game_name, type=1, url=stream_url))

    def variable_code(self):
        """
        Function that makes Certain things on the on_ready event only happen 1 time only. (eg the logged in printing
        stuff)
        :return: Nothing.
        """
        self.logged_in = True


class BotLogin:
    """
    Base Class for getting the bot login.
    """
    def __init__(self):
        self.bot = BotData()

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
