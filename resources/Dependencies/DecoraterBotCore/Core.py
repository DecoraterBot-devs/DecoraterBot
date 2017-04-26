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


class GitHubRoute:
    """gets the route information to the an github resource/file."""
    HEAD = "https://raw.githubusercontent.com/"

    def __init__(self, user : str, repo : str,
                 branch : str, filename : str):
        self.url = (self.HEAD + user + "/" +
                    repo + "/" + branch + "/" +
                    filename)


class PluginData:
    """
    Stores the data to plugins.
    """
    def __init__(self, plugincode=None, version=None,
                 textjson=None):
        self.plugincode = plugincode
        self.version = version
        self.textjson = textjson


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
        self.PluginConfigReader = BotConfigReader.PluginConfigReader
        self.PluginTextReader = BotConfigReader.PluginTextReader
        self.somebool = False
        self.reload_normal_commands = False
        self.reload_voice_commands = False
        self.reload_reason = None
        self.initial_rejoin_voice_channel = True
        self.desmod = None
        self.desmod_new = None
        self.rejoin_after_reload = False
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
        self.initial_plugins_cogs = self.BotConfig.default_plugins
        for plugins_cog in self.initial_plugins_cogs:
            ret = self.containers.load_plugin(self, plugins_cog)
            if isinstance(ret, str):
                print(ret)
        self.disabletinyurl = disabletinyurl
        self.TinyURL = TinyURL
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

    def make_voice_info(self, server_id, textchannel_id,
                        voice_id):
        """
        Makes the Text, Voice Channel, and Server objects
        with the cached id's for Voice Channels.
        """
        str(self)
        retserver = discord.server.Server(id=server_id)
        rettextchannel = discord.channel.Channel(
            server=retserver, id=textchannel_id)
        retvoicechannel = discord.channel.Channel(
            server=retserver, id=voice_id)
        return retvoicechannel, rettextchannel

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

    @staticmethod
    def make_version(pluginname, pluginversion,
                     version=None):
        """
        Makes or remakes the contents to the plugin list
        json that stores the installed versions.

        Used for installing / updating plugins.
        """
        if version is None:
            version = {}
        version[pluginname] = {}
        version[pluginname]['version'] = pluginversion
        return version

    async def request_repo(self, pluginname):
        """
        requests the bot's plugin
        repository for an particualar plugin.
        """
        url = (
            GitHubRoute(
                "DecoraterBot-devs", "DecoraterBot-cogs",
                "master", "cogslist.json")).url
        data = await self.http.session.get(url)
        resp1 = await data.json(content_type='text/plain')
        version = resp1[pluginname]['version']
        url2 = resp1[pluginname]['downloadurl']
        url3 = resp1[pluginname]['textjson']
        data2 = await session.get(url2)
        data3 = await session.get(url3)
        plugincode = await data2.text()
        textjson = await data3.text()
        return PluginData(plugincode=plugincode,
                          version=version,
                          textjson=textjson)

    async def checkupdate(self, pluginname):
        """
        checks a plugin provided for updates.
        :returns: string considing of plugin's name
        and plugin's current version.
        """
        pluginversion = None  # for now until this is complete.
        requestrepo = await self.request_repo(pluginname)
        if requestrepo.version != pluginversion:
            # return every instance of 'PluginData'.
            return requestrepo

    async def checkupdates(self, pluginlist):
       """
       Checks for updates for plugins
       in the plugin list.
       """
       update_list = []
       for plugin in pluginlist:
           update_list.append(await self.checkupdate(plugin))
       # so bot can know which plugins have updates.
       return update_list

    async def install_plugin(self, pluginname):
        """
        installs a plugin provided.
        Also gets and sets an cached
        version of them too.
        """
        # TODO: Finish this.
        pass

    async def install_plugins(self, pluginnames):
        """
        installs all the plugins listed.
        """
        for pluginname in pluginnames:
            # install each plugin individually.
            self.install_plugin(pluginname)

    @staticmethod
    def changewindowsize():
        """
        Changes the Console's size.
        :return: Nothing.
        """
        consolechange.consolesize(80, 23)

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

    def login_helper(self):
        """
        Bot Login Helper.
        :return: Nothing.
        """
        while True:
            ret = self.login_info()
            if ret is not None and ret is not -1:
                break

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
