# coding=utf-8
"""
    DecoraterBot's source is protected by Cheese.lab industries Inc. Even though it is Open Source
    any and all users waive the right to say that this bot's code was stolen when it really was not.
    Me @Decorater the only core developer of this bot do not take kindly to those false Allegations.
    it would piss any DEVELOPER OFF WHEN THEY SPEND ABOUT A YEAR CODING STUFF FROM SCRATCH AND THEN BE ACCUSED OF SHIT LIKE THIS.
    
    So, do not do it. If you do Cheese.lab Industries Inc. Can and Will do after you for such cliams that it deems untrue.
    
    Cheese.lab industries Inc. Belieces in the rights of Original Developers of bots. They do not take kindly to BULLSHIT.
    
    Any and all Developers work all the time, many of them do not get paid for their hard work.
    
    I am one of those who did not get paid even though I am the original Developer I coded this bot from the bottom with no lines of code at all.
    
    And how much money did I get from it for my 11 months or so of working on it? None- yeah thats right 0$ how pissed can someone be?
    Exactly I have over stretched my relatives money that they paid for Internet and power for my computer so that way I can code my bot.
    
    However shit does go out of the Fan with a possible 600$ or more that my Laptop Drastically needs to Repairs as it is 10 years old and is falling apart
    
    I am half tempted myself to pulling this bot from github and making it on patrion that boobot is also on to help me with my development needs.
    
    So, as such I accept issue requests, but please do not give me bullshit I hate it as it makes everything worse than the way it is.
    
    You do have the right however to:
        -> Contribute to the bot's development.
        -> fix bugs.
        -> add commands.
        -> help finish the per server config (has issues)
        -> update the Voice commands to be better (and not use globals which is 1 big thing that kills it).

    But keep in mind any and all Changes you make can and will be property of Cheese.lab Industries Inc.
"""
import discord
import asyncio
import os
import os.path
import sys
import json
import io
from discord.__init__ import __version__
from colorama import init
from colorama import Fore, Back, Style
from discord.ext import commands

init()

consoledatafile = io.open(sys.path[0] + '\\resources\\ConfigData\\ConsoleWindow.json', 'r')
consoletext = json.load(consoledatafile)

PATH = sys.path[0] + '\\resources\\ConfigData\\Credentials.json'

global reconnects
# noinspection PyRedeclaration
reconnects = 0
global is_bot_logged_in
# noinspection PyRedeclaration
is_bot_logged_in = False


class bot_data:
    """
        This Class is for Internal Use only!!!
    """
    def __init__(self):
        pass

    def login_info_code(self, client):
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
                reconnects = reconnects + 1
                if reconnects != 0:
                    print('Bot is currently reconnecting for {0} times.'.format(str(reconnects)))
                    # sleeptime = reconnects * 5
                    # asyncio.sleep(sleeptime)
                    self.login_info_code(client)
            if is_bot_logged_in:
                if not client.is_logged_in:
                    pass
                else:
                    reconnects = reconnects + 1
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
        global logged_in
        if logged_in:
            logged_in = False
            botmessagesdata = io.open(sys.path[0] + '\\resources\\ConfigData\\BotMessages.json', 'r')
            botmessages = json.load(botmessagesdata)
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

    def variable_code(self):
        global logged_in
        logged_in = True


class BotLogin:
    def __init__(self):
        self.bot = bot_data()

    def login_info(self, client):
        self.bot.login_info_code(client)

    @asyncio.coroutine
    def on_login(self, client):
        yield from self.bot.on_login_code(client)

    def variable(self):
        self.bot.variable_code()
