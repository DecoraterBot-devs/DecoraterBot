# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import os
import ctypes
import sys
import time
import json
import traceback
import asyncio

import aiohttp
import discord
from discord.ext import commands
from colorama import Fore, Back, Style
from colorama import init
import consolechange
try:
    import TinyURL
    disabletinyurl = False
except ImportError:
    print_data_001 = 'TinyURL for Python 3.x was not installed.\n' \
                     'It can be found at: https://github.com/AraHaan/Tin' \
                     'yURL\nDisabled the tinyurl command for now.'
    print(print_data_001)
    disabletinyurl = True
    TinyURL = None

from .BotErrors import *
try:
    from . import BotPMError
except ImportError:
    print('Some Unknown thing happened which made a critical bot c'
          'ode file unable to be found.')
    BotPMError = None
from . import BotConfigReader
from .BotLogs import *
from . import containers
# from .web.database import Db
# from .web.datadog import DDAgent


__all__ = ['main', 'BotClient']

config = BotConfigReader.BotCredentialsVars()


class YTDLLogger(object):
    """
    Class for Silencing all of the Youtube_DL Logging stuff that defaults to
    console.
    """

    def __init__(self, bot):
        self.bot = bot

    def log_file_code(self, meth, msg):
        """
        Logs data to file (if set).
        :param meth: Method name.
        :param msg: message.
        :return: Nothing.
        """
        if meth is not '':
            if meth == 'ytdl_debug':
                logfile = '{0}{1}resources{1}Logs{1}ytdl_deb' \
                          'ug_logs.txt'.format(self.bot.path, self.bot.sepa)
                try:
                    file = open(logfile, 'a', encoding='utf-8')
                    size = os.path.getsize(logfile)
                    if size >= 32102400:
                        file.seek(0)
                        file.truncate()
                    file.write(msg + '\n')
                    file.close()
                except PermissionError:
                    return
            elif meth == 'ytdl_warning':
                logfile2 = '{0}{1}resources{1}Logs{1}ytdl_warnin' \
                           'g_logs.txt'.format(self.bot.path, self.bot.sepa)
                try:
                    file2 = open(logfile2, 'a', encoding='utf-8')
                    size = os.path.getsize(logfile2)
                    if size >= 32102400:
                        file2.seek(0)
                        file2.truncate()
                    file2.write(msg + '\n')
                    file2.close()
                except PermissionError:
                    return
            elif meth == 'ytdl_error':
                logfile3 = '{0}{1}resources{1}Logs{1}ytdl_er' \
                           'ror_logs.txt'.format(self.bot.path, self.bot.sepa)
                try:
                    file3 = open(logfile3, 'a', encoding='utf-8')
                    size = os.path.getsize(logfile3)
                    if size >= 32102400:
                        file3.seek(0)
                        file3.truncate()
                    file3.write(msg + '\n')
                    file3.close()
                except PermissionError:
                    return
            elif meth == 'ytdl_info':
                logfile4 = '{0}{1}resources{1}Logs{1}ytd' \
                           'l_info_logs.txt'.format(self.bot.path,
                                                    self.bot.sepa)
                try:
                    file4 = open(logfile4, 'a', encoding='utf-8')
                    size = os.path.getsize(logfile4)
                    if size >= 32102400:
                        file4.seek(0)
                        file4.truncate()
                    file4.write(msg + '\n')
                    file4.close()
                except PermissionError:
                    return
        else:
            return

    def info(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or
        silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_ytdl:
            self.log_file_code('ytdl_info', msg)
        else:
            pass

    def debug(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or
        silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_ytdl:
            self.log_file_code('ytdl_debug', msg)
        else:
            pass

    def warning(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or
        silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_ytdl:
            self.log_file_code('ytdl_warning', msg)
        else:
            pass

    def error(self, msg):
        """
        Reroutes the Youtube_DL Messages of this type to teither a file or
        silences them.
        :param msg: Message.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_ytdl:
            self.log_file_code('ytdl_error', msg)
        else:
            pass


class BotClient(commands.Bot):
    """
    Bot Main client Class.
    This is where the Events are Registered.
    """
    logged_in = False

    def __init__(self, **kwargs):
        self.BotPMError = BotPMError
        self.BotConfig = config
        self.sepa = os.sep
        self.bits = ctypes.sizeof(ctypes.c_voidp)
        self.containers = containers
        self.commands_list = []
        self.YTDLLogger = YTDLLogger
        self.platform = None
        if self.bits == 4:
            self.platform = 'x86'
        elif self.bits == 8:
            self.platform = 'x64'
        self.path = sys.path[0]
        self.botbanslist = open('{0}{1}resources{1}Conf'
                                'igData{1}BotBanned.json'.format(self.path,
                                                                 self.sepa))
        self.banlist = json.load(self.botbanslist)
        self.botbanslist.close()
        self.consoledatafile = open('{0}{1}resources{1}'
                                    'ConfigData{1}ConsoleWindow.{2}.'
                                    'json'.format(self.path, self.sepa,
                                                  self.BotConfig.language))
        self.consoletext = json.load(self.consoledatafile)
        self.consoledatafile.close()
        try:
            self.ignoreslistfile = open('{0}{1}resources{1}ConfigDa'
                                        'ta{1}IgnoreList.'
                                        'json'.format(self.path, self.sepa))
            self.ignoreslist = json.load(self.ignoreslistfile)
            self.ignoreslistfile.close()
        except FileNotFoundError:
            print(str(self.consoletext['Missing_JSON_Errors'][0]))
            sys.exit(2)
        # deprecated, will be removed when remaing default cogs become plugins.
        self.botmessagesdata = open('{0}{1}resources{1}ConfigD'
                                    'ata{1}BotMessages.{2}.'
                                    'json'.format(self.path, self.sepa,
                                                  self.BotConfig.language))
        # deprecated, will be removed when remaing default cogs become plugins.
        self.botmessages = json.load(self.botmessagesdata)
        # deprecated, will be removed when remaing default cogs become plugins.
        self.botmessagesdata.close()
        self.version = str(self.consoletext['WindowVersion'][0])
        self.start = time.time()
        # Bool to help let the bot know weather or not to actually print
        # the logged in stuff.
        self.logged_in_ = BotClient.logged_in
        # default to True in case options are not present in Credentials.json
        self.reconnects = 0
        # Will Always be True to prevent the Error Handler from Causing Issues
        # later.
        # Well only if the PM Error handler is False.
        self.enable_error_handler = True
        self.PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(
            self.path, self.sepa)
        self.DBLogs = BotLogger(self)
        # for the bot's plugins to be able to read their text json files.
        self.PluginTextReader = BotConfigReader.PluginTextReader
        self.somebool = False
        self.reload_normal_commands = False
        self.reload_voice_commands = False
        self.reload_reason = None
        self.initial_rejoin_voice_channel = True
        self.desmod = None
        self.desmod_new = None
        self.rejoin_after_reload = False
        # For Console Window size. (windows only)
        self.cmd = "mode con: cols=80 lines=23"
        # The platform list I have so far.
        if not (sys.platform.startswith('win') or sys.platform.startswith(
                'linux')):
            self.platerrormsg = str(
                self.consoletext['Unsupported_Platform'][0])
            raise UnsupportedPlatform(self.platerrormsg.format(sys.platform))
        # DecoraterBot Necessities.
        self.asyncio_logger()
        self.discord_logger()
        self.changewindowtitle()
        # self.changewindowsize()
        super(BotClient, self).__init__(**kwargs)
        self.initial_plugins_cogs = [
            'logs',
            'moderation',
            'report',
            'voice'
        ]
        for plugins_cog in self.initial_plugins_cogs:
            ret = self.containers.load_plugin(self, plugins_cog)
            if isinstance(ret, str):
                print(ret)
        self.initial_commands_cogs = [
            'botcorecommands',
            'botcommands'
        ]
        for commands_cog in self.initial_commands_cogs:
            ret = self.containers.load_command(self, commands_cog)
            if isinstance(ret, str):
                print(ret)
        self.disabletinyurl = disabletinyurl
        self.TinyURL = TinyURL
        self.version = str(self.consoletext['WindowVersion'][0])
        self.rev = str(self.consoletext['Revision'][0])
        self.sourcelink = str(self.botmessages['source_command_data'][0])
        self.othercommands = str(
            self.botmessages['commands_command_data'][1])
        self.commandstuff = str(
            self.botmessages['commands_command_data'][4])
        self.botcommands = str(
            self.botmessages['commands_command_data'][
                0]) + self.othercommands + self.commandstuff
        self.botcommands_without_other_stuff = (str(
            self.botmessages['commands_command_data'][0]) +
                                                self.othercommands)
        self.othercommandthings = str(
            self.botmessages['commands_command_data'][4]) + str(
            self.botmessages['commands_command_data'][5])
        self.botcommandswithturl_01 = str(
            self.botmessages['commands_command_data'][
                3]) + self.othercommandthings
        self.botcommandswithtinyurl = (self.botcommands_without_other_stuff +
                                       self.botcommandswithturl_01)
        self.changelog = str(self.botmessages['changelog_data'][0])
        self.info = "``" + str(self.consoletext['WindowName'][
                                   0]) + self.version + self.rev + "``"
        self.botcommandsPM = str(
            self.botmessages['commands_command_data'][2])
        self.commandturlfix = str(
            self.botmessages['commands_command_data'][5])
        self.botcommandsPMwithtinyurl = self.botcommandsPM + str(
            self.botmessages['commands_command_data'][
                3]) + self.commandturlfix
        self.sent_prune_error_message = False
        self.tinyurlerror = False
        self.link = None
        self.member_list = []
        self.hook_url = None
        self.payload = {}
        self.header = {}
        self.resolve_send_message_error = (
            self.BotPMError.resolve_send_message_error)
        self.remove_command("help")
        init()
        self.variable()
        self.credits = BotConfigReader.CreditsReader(file="credits.json")
        # self.db = Db(self.redis_url, self.mongo_url, self.loop)
        # self.plugin_manager = PluginManager(self)
        # self.plugin_manager.load_all()
        self.last_messages = []
        # self.stats = DDAgent(self.dd_agent_url)
        self.is_bot_logged_in = False
        self.login_helper()  # handles login.

    @staticmethod
    def make_voice_info(server_id, textchannel_id, voice_id):
        """
        Makes the Text, Voice Channel, and Server objects
        with the cached id's for Voice Channels.
        """
        retserver = discord.server.Server(id=server_id)
        rettextchannel = discord.channel.Channel(
            server=retserver, id=textchannel_id)
        retvoicechannel = discord.channel.Channel(
            server=retserver, id=voice_id)
        return retserver, rettextchannel, retvoicechannel

    def add_commands(self, data):
        """Adds commands to commands_list."""
        for command in data:
            self.commands_list.append(command)

    def remove_commands(self, data):
        """Removes commands from commands_list."""
        for command in data:
            self.commands_list.remove(command)

    def changewindowtitle(self):
        """
        Changes the console's window Title.
        :return: Nothing.
        """
        consolechange.consoletitle(str(self.consoletext['WindowName'][0]) + self.version)

    def changewindowsize(self):
        """
        Changes the Console's size.
        :return: Nothing.
        """
        # the Following is windows only.
        os.system(self.cmd)

    def discord_logger(self):
        """
        Logger Data.
        :return: Nothing.
        """
        if self.BotConfig.discord_logger:
            self.DBLogs.set_up_discord_logger()

    def asyncio_logger(self):
        """
        Asyncio Logger.
        :return: Nothing.
        """
        if self.BotConfig.asyncio_logger:
            self.DBLogs.set_up_asyncio_logger()

    # Helpers.

    async def mention_ban_helper(self, message):
        """
        Bot Commands.
        :param message: Messages.
        :return: Nothing.
        """
        if message.author.id == self.user.id:
            return
        if message.channel.server.id == "105010597954871296":
            return
        if message.author.id == self.owner_id:
            return
        else:
            try:
                await self.ban(message.author)
                try:
                    message_data = str(
                        self.botmessages['mention_spam_ban'][0]).format(
                        message.author)
                    await self.send_message(message.channel,
                                            content=message_data)
                except discord.errors.Forbidden:
                    await self.BotPMError.resolve_send_message_error_old(
                        self, message)
            except discord.errors.Forbidden:
                try:
                    msgdata = str(
                        self.botmessages['mention_spam_ban'][1]).format(
                        message.author)
                    message_data = msgdata
                    await self.send_message(message.channel,
                                            content=message_data)
                except discord.errors.Forbidden:
                    await self.BotPMError.resolve_send_message_error_old(
                        self, message)
            except discord.HTTPException:
                try:
                    msgdata = str(
                        self.botmessages['mention_spam_ban'][2]).format(
                        message.author)
                    message_data = msgdata
                    await self.send_message(message.channel,
                                            content=message_data)
                except discord.errors.Forbidden:
                    await self.BotPMError.resolve_send_message_error_old(
                        self, message)

    async def bot_mentioned_helper(self, message):
        """
        Bot Commands.
        :param message: Messages.
        :return: Nothing.
        """
        if message.author.id in self.banlist['Users']:
            return
        elif message.author.bot:
            return
        else:
            for command in self.commands_list:
                if message.content.startswith(command):
                    return
                else:
                    break
            else:
                if message.channel.server.id == "140849390079180800":
                    return
                elif message.author.id == self.user.id:
                    return
                elif message.channel.server.id == "110373943822540800":
                    if message.author.id == "103607047383166976":
                        return
                    else:
                        info2 = str(
                            self.botmessages['On_Bot_Mention_Message_Data'][
                                0]).format(message.author)
                        await self.send_message(message.channel, content=info2)
                elif message.channel.server.id == '101596364479135744':
                    if message.author.id == "110368240768679936":
                        return
                    else:
                        info2 = str(
                            self.botmessages['On_Bot_Mention_Message_Data'][
                                0]).format(message.author)
                        await self.send_message(message.channel, content=info2)
                else:
                    info2 = str(
                        self.botmessages['On_Bot_Mention_Message_Data'][
                            0]).format(message.author)
                    try:
                        await self.send_message(message.channel, content=info2)
                    except discord.errors.Forbidden:
                        await self.BotPMError.resolve_send_message_error_old(
                            self, message)

    def login_helper(self):
        """
        Bot Login Helper.
        :return: Nothing.
        """
        while True:
            ret = self.login_info()
            if ret is not None and ret is not -1:
                break

    def game_command_helper(self, ctx):
        """
        Bot `::game` command Helper.
        :param ctx: Message Context.
        :return: game data.
        """
        desgame = ctx.message.content[len(ctx.prefix + "game "):].strip()
        desgametype = None
        stream_url = None
        desgamesize = len(desgame)
        if desgamesize > 0:
            if len(ctx.message.mentions) > 0:
                for x in ctx.message.mentions:
                    desgame = desgame.replace(x.mention, x.name)
            if desgame.find(" | type=") is not -1:
                if desgame.find(" | type=1") is not -1:
                    desgame = desgame.replace(" | type=1", "")
                    desgametype = 1
                    stream_url = self.BotConfig.twitch_url
                    return desgame, desgametype, stream_url, desgamesize
                elif desgame.find(" | type=2") is not -1:
                    desgame = desgame.replace(" | type=2", "")
                    desgametype = 2
                    stream_url = self.BotConfig.youtube_url
                    return desgame, desgametype, stream_url, desgamesize
            else:
                return desgame, desgametype, stream_url, desgamesize
        else:
            desgame = None
            return desgame, desgametype, stream_url, desgamesize

    async def cheesy_commands_helper(self, message):
        """
        Listens fCheese.lab Specific Server commands.
        :param message: Message.
        :return: Nothing.
        """
        serveridslistfile = open(
            '{0}{1}resources{1}ConfigData{1}serverconfigs{1}servers.'
            'json'.format(self.path, self.sepa))
        serveridslist = json.load(serveridslistfile)
        serveridslistfile.close()
        serverid = str(serveridslist['config_server_ids'][0])
        file_path = (
            '{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}'
            'verifications{0}'.format(self.sepa, serverid))
        filename_1 = 'verifycache.json'
        filename_2 = 'verifycommand.json'
        filename_3 = 'verifyrole.json'
        filename_4 = 'verifymessages.json'
        filename_5 = 'verifycache.json'
        joinedlistfile = open(self.path + file_path + filename_1)
        newlyjoinedlist = json.load(joinedlistfile)
        joinedlistfile.close()
        memberjoinverifymessagefile = open(self.path + file_path + filename_2)
        memberjoinverifymessagedata = json.load(memberjoinverifymessagefile)
        memberjoinverifymessagefile.close()
        memberjoinverifyrolefile = open(self.path + file_path + filename_3)
        memberjoinverifyroledata = json.load(memberjoinverifyrolefile)
        memberjoinverifyrolefile.close()
        memberjoinverifymessagefile2 = open(self.path + file_path + filename_4)
        memberjoinverifymessagedata2 = json.load(memberjoinverifymessagefile2)
        memberjoinverifymessagefile2.close()
        role_name = str(memberjoinverifyroledata['verify_role_id'][0])
        msg_command = str(memberjoinverifymessagedata['verify_command'][0])
        try:
            if '>' or '<' or '`' in message.content:
                msgdata = message.content.replace('<', '').replace('>',
                                                                   '').replace(
                    '`', '')
            else:
                msgdata = message.content
            if msg_command == msgdata:
                if message.author.id in newlyjoinedlist[
                        'users_to_be_verified']:
                    await self.delete_message(message)
                    role2 = discord.utils.find(
                        lambda role: role.id == role_name,
                        message.channel.server.roles)
                    msg_data = str(
                        memberjoinverifymessagedata2['verify_messages'][
                            1]).format(
                        message.server.name)
                    await self.add_roles(message.author, role2)
                    await self.send_message(message.author, content=msg_data)
                    newlyjoinedlist['users_to_be_verified'].remove(
                        message.author.id)
                    json.dump(newlyjoinedlist,
                              open(self.path + file_path + filename_5, "w"))
                else:
                    await self.delete_message(message)
                    await self.send_message(message.channel, content=str(
                        memberjoinverifymessagedata2['verify_messages'][2]))
            else:
                if message.author.id != self.user.id:
                    if message.author.id in newlyjoinedlist[
                            'users_to_be_verified']:
                        await self.delete_message(message)
                        await self.send_message(message.channel, content=str(
                            memberjoinverifymessagedata2['verify_messages'][
                                3]).format(message.author.mention))
        except NameError:
            await self.send_message(message.channel, content=str(
                memberjoinverifymessagedata2['verify_messages'][4]).format(
                message.author.mention))

    # Login stuff.

    async def __ffs__(self, *args, **kwargs):
        await self.login(*args, **kwargs)
        await self.connect()

    def login_info(self):
        """
        Allows the bot to Connect / Reconnect.
        :return: Nothing.
        """
        if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
            try:
                if (self.BotConfig.discord_user_email and
                        self.BotConfig.discord_user_password is not None):
                    self.is_bot_logged_in = True
                    self.loop.run_until_complete(
                        self.__ffs__(self.BotConfig.discord_user_email,
                                     self.BotConfig.discord_user_password))
                elif self.BotConfig.bot_token is not None:
                    self.is_bot_logged_in = True
                    self.loop.run_until_complete(self.__ffs__(
                        self.BotConfig.bot_token))
            except discord.errors.GatewayNotFound:
                print(str(self.consoletext['Login_Gateway_No_Find'][0]))
                return -2
            except discord.errors.LoginFailure as e:
                if str(e) == "Improper credentials have been passed.":
                    print(str(self.consoletext['Login_Failure'][0]))
                    return -2
                elif str(e) == "Improper token has been passed.":
                    print(str(self.consoletext['Invalid_Token'][0]))
                    sys.exit(2)
            except TypeError:
                pass
            except KeyboardInterrupt:
                pass
            except asyncio.futures.InvalidStateError:
                self.reconnects += 1
                if self.reconnects != 0:
                    print(
                        'Bot is currently reconnecting for {0} times.'.format(
                            str(self.reconnects)))
                    return -1
            except aiohttp.ClientResponseError:
                self.reconnects += 1
                if self.reconnects != 0:
                    print(
                        'Bot is currently reconnecting for {0} times.'.format(
                            str(self.reconnects)))
                    return -1
            except aiohttp.ClientOSError:
                self.reconnects += 1
                if self.reconnects != 0:
                    print(
                        'Bot is currently reconnecting for {0} times.'.format(
                            str(self.reconnects)))
                    return -1
            if self.is_bot_logged_in:
                if not self.is_logged_in:
                    pass
                else:
                    self.reconnects += 1
                    if self.reconnects != 0:
                        print(
                            'Bot is currently reconnecting for {0} '
                            'times.'.format(str(self.reconnects)))
                        return -1
        else:
            print(str(self.consoletext['Credentials_Not_Found'][0]))
            sys.exit(2)

    async def on_login(self):
        """
        Function that does the on_ready event stuff after logging in.
        :return: Nothing.
        """
        if self.logged_in_:
            self.logged_in_ = False
            message_data = str(self.botmessages['On_Ready_Message'][0])
            try:
                await self.send_message(
                    discord.Object(id='118098998744580098'),
                    content=message_data)
            except discord.errors.Forbidden:
                return
            try:
                await self.send_message(
                    discord.Object(id='103685935593435136'),
                    content=message_data)
            except discord.errors.Forbidden:
                return
            bot_name = self.user.name
            print(Fore.GREEN + Back.BLACK + Style.BRIGHT + str(
                self.consoletext['Window_Login_Text'][0]).format(
                bot_name, self.user.id, discord.__version__))
            sys.stdout = open(
                '{0}{1}resources{1}Logs{1}console.log'.format(self.path,
                                                              self.sepa), 'w')
            sys.stderr = open(
                '{0}{1}resources{1}Logs{1}unhandled_tracebacks.log'.format(
                    self.path, self.sepa),
                'w')
        if not self.logged_in_:
            game_name = str(self.consoletext['On_Ready_Game'][0])
            stream_url = "https://twitch.tv/decoraterbot"
            await self.change_presence(
                game=discord.Game(name=game_name, type=1, url=stream_url))

    def variable(self):
        """
        Function that makes Certain things on the on_ready event only happen 1
        time only. (e.g. the logged in printing stuff)
        :return: Nothing.
        """
        if not BotClient.logged_in:
            BotClient.logged_in = True
            self.logged_in_ = True

    # Cache Cleanup.

    async def verify_cache_cleanup_2(self, member):
        """
        Cleans Up Verify Cache.
        :param member: Member.
        :return: Nothing.
        """
        try:
            serveridslistfile = open(
                '{0}{1}resources{1}ConfigData{1}serverconfigs{1}'
                'servers.json'.format(self.path, self.sepa))
            serveridslist = json.load(serveridslistfile)
            serveridslistfile.close()
            serverid = str(serveridslist['config_server_ids'][0])
            file_path = (
                '{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}'
                'verifications{0}'.format(self.sepa, serverid))
            filename_1 = 'verifycache.json'
            joinedlistfile = open(self.path + file_path + filename_1)
            newlyjoinedlist = json.load(joinedlistfile)
            joinedlistfile.close()
            if member.id in newlyjoinedlist['users_to_be_verified']:
                await self.send_message(
                    discord.Object(id='141489876200718336'),
                    content="{0} has left the {1} Server.".format(
                        member.mention, member.server.name))
                newlyjoinedlist['users_to_be_verified'].remove(member.id)
                file_name = "{0}verifications{0}verifycache.json".format(
                    self.sepa)
                filename = "{0}{1}resources{1}ConfigData{1}serverconfigs{1}" \
                           "71324306319093760{2}".format(self.path, self.sepa,
                                                         file_name)
                json.dump(newlyjoinedlist, open(filename, "w"))
        except Exception as e:
            funcname = 'verify_cache_cleanup_2'
            tbinfo = str(traceback.format_exc())
            self.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def verify_cache_cleanup(self, member):
        """
        Cleans Up Verify Cache.
        :param member: Member.
        :return: Nothing.
        """
        try:
            serveridslistfile = open(
                '{0}{1}resources{1}ConfigData{1}serverconfigs{1}'
                'servers.json'.format(
                    self.path, self.sepa))
            serveridslist = json.load(serveridslistfile)
            serveridslistfile.close()
            serverid = str(serveridslist['config_server_ids'][0])
            file_path = '{0}resources{0}ConfigData{0}serverconfigs{0}{1}' \
                        '{0}verifications{0}'.format(self.sepa, serverid)
            filename_1 = 'verifycache.json'
            joinedlistfile = open(self.path + file_path + filename_1)
            newlyjoinedlist = json.load(joinedlistfile)
            joinedlistfile.close()
            if member.id in newlyjoinedlist['users_to_be_verified']:
                newlyjoinedlist['users_to_be_verified'].remove(member.id)
                file_name = "{0}verifications{0}verifycache.json".format(
                    self.sepa)
                filename = "{0}{1}resources{1}ConfigData{1}serverconfigs" \
                           "{1}71324306319093760{2}".format(self.path,
                                                            self.sepa,
                                                            file_name)
                json.dump(newlyjoinedlist, open(filename, "w"))
        except Exception as e:
            funcname = 'verify_cache_cleanup'
            tbinfo = str(traceback.format_exc())
            self.DBLogs.on_bot_error(funcname, tbinfo, e)


def main():
    """
    EntryPoint to DecoraterBot.
    :return: Nothing.
    """
    if config.shards > 0:
        BotClient(command_prefix=config.bot_prefix,
                  shard_id=config.run_on_shard,
                  shard_count=config.shards,
                  description=config.description,
                  pm_help=False)
    else:
        BotClient(command_prefix=config.bot_prefix,
                  description=config.description,
                  pm_help=False)
