# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import os
import sys
import traceback
import time
import asyncio

import aiohttp
import discord
from discord.ext import commands
import consolechange
import dbapi
from DecoraterBotUtils.BotErrors import *
from DecoraterBotUtils.utils import *
try:
    import TinyURL
    disabletinyurl = False
except ImportError:
    print_data_001 = 'TinyURL for Python 3.x was not installed.\n' \
                     'It can be installed by running: pip install' \
                     ' --upgrade TinyURL3\nDisabled the tinyurl ' \
                     'command for now.'
    print(print_data_001)
    disabletinyurl = True
    TinyURL = None


__all__ = ['main', 'BotClient']

config = BotCredentialsVars()


class BotClient(commands.Bot):
    """
    Bot Main client Class.
    This is where the Events are Registered.
    """
    logged_in = False

    def __init__(self, **kwargs):
        self.BotPMError = BotPMError(self)
        self._start = time.time()
        self.logged_in_ = BotClient.logged_in
        self._rec = ReconnectionHelper()
        self.PATH = os.path.join(
            sys.path[0], 'resources', 'ConfigData', 'Credentials.json')
        self.somebool = False
        self.reload_normal_commands = False
        self.reload_voice_commands = False
        self.reload_reason = None
        self.initial_rejoin_voice_channel = True
        self.desmod = None
        self.desmod_new = None
        self.rejoin_after_reload = False
        super(BotClient, self).__init__(**kwargs)
        self.dbapi = dbapi.DBAPI(self, self.BotConfig.api_token)
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
        self.is_bot_logged_in = False
        self.call_all()

    # Properties.

    @property
    def version(self):
        """
        returns the bot's version number.
        """
        return self.consoletext['WindowVersion'][0]

    @property
    def BotConfig(self):
        """
        Reads the bot's config data.
        """
        return config

    @property
    def consoletext(self):
        """
        returns the bot's
        console text.
        """
        consoledata = PluginConfigReader(file='ConsoleWindow.json')
        consoledata = consoledata[self.BotConfig.language]
        return consoledata

    @property
    def banlist(self):
        """
        returns the list of users banned
        from using the bot.
        """
        type(self)
        return PluginConfigReader(
            file='BotBanned.json')

    @property
    def uptime_count_begin(self):
        """
        returns the begin time.
        """
        return self._start

    @property
    def commands_list(self):
        """
        retrieves a list of all of the bot's registered commands.
        """
        plugin_list = []
        for command in self.commands:
            plugin_list.append(command)
        return plugin_list

    @property
    def credits(self):
        """
        returns the stuff that the Credits reader returns.
        """
        return CreditsReader(file="credits.json")

    @property
    def ignoreslist(self):
        """
        returns the current ignores list.
        """
        try:
            ret = PluginConfigReader(file='IgnoreList.json')
        except FileNotFoundError:
            ret = None
            print(str(self.consoletext['Missing_JSON_Errors'][0]))
            sys.exit(2)
        return ret

    # wraps all usage of send_message.

    async def send(self, message=None, ctx=None,
                   *args, **kwargs):
        """
        wraps send_message.
        """
        try:
            await self.send_message(
                *args, **kwargs)
        except discord.errors.Forbidden:
            if ctx is not None:
                # TODO: Actually raise an exception here.
                await self.BotPMError.resolve_send_message_error(
                    ctx)
            else:
                # TODO: Finish this.
                pass

    def call_all(self):
        """
        calls all functions that __init__ used to
        call except for super.
        """
        # DecoraterBot Necessities.
        self.asyncio_logger()
        self.discord_logger()
        self.changewindowtitle()
        # self.changewindowsize()
        self.remove_command("help")
        self.load_all_default_plugins()
        self.variable()
        self.login_helper()  # handles login.

    # Plugin loading/unloading/reloading.

    def load_all_default_plugins(self):
        """
        Handles loading all plugins that __init__
        used to load up.
        """
        for plugins_cog in self.BotConfig.default_plugins:
            ret = self.load_plugin(plugins_cog)
            if isinstance(ret, str):
                print(ret)

    def load_bot_extension(self, extension_full_name):
        """
        loads an bot extension module.
        """
        try:
            self.load_extension(extension_full_name)
        except Exception:
            return str(traceback.format_exc())

    def unload_bot_extension(self, extension_full_name):
        """
        unloads an bot extension module.
        """
        self.unload_extension(extension_full_name)

    def load_plugin(self, plugin_name, raiseexec=True):
        """
        Loads up a plugin in the plugins folder in DecoraterBotCore.
        """
        pluginfullname = get_plugin_full_name(plugin_name)
        if pluginfullname is None:
            if raiseexec:
                raise ImportError(
                    "Plugin Name cannot be empty.")
        err = self.load_bot_extension(pluginfullname)
        if err is not None:
            return err

    def unload_plugin(self, plugin_name, raiseexec=True):
        """
        Unloads a plugin in the plugins folder in DecoraterBotCore.
        """
        pluginfullname = get_plugin_full_name(plugin_name)
        if pluginfullname is None:
            if raiseexec:
                raise CogUnloadError(
                    "Plugin Name cannot be empty.")
        self.unload_bot_extension(pluginfullname)

    def reload_plugin(self, plugin_name):
        """
        Reloads a plugin in the plugins folder in DecoraterBotCore.
        """
        self.unload_plugin(plugin_name, raiseexec=False)
        err = self.load_plugin(plugin_name)
        if err is not None:
            return err

    # Console Window.

    def changewindowtitle(self):
        """
        Changes the console's window Title.
        """
        consolechange.consoletitle(
            self.consoletext['WindowName'][0] + self.version)

    def changewindowsize(self):
        """
        Changes the Console's size.
        """
        # not used but avoids issues with this being an classmethod.
        type(self)
        consolechange.consolesize(80, 23)

    # Loggers.

    def discord_logger(self):
        """
        Logger Data.
        """
        if self.BotConfig.discord_logger:
            self.set_up_discord_logger()

    def asyncio_logger(self):
        """
        Asyncio Logger.
        """
        if self.BotConfig.asyncio_logger:
            self.set_up_asyncio_logger()

    def set_up_loggers(self, loggers=None):
        """
        Logs Events from discord and/or asyncio stuff.
        """
        if loggers is not None:
            if loggers == 'discord':
                logger = logging.getLogger('discord')
                logger.setLevel(logging.DEBUG)
                handler = logging.FileHandler(
                    filename=os.path.join(
                        sys.path[0], 'resources', 'Logs', 'discordpy.log'),
                    encoding='utf-8', mode='w')
                handler.setFormatter(logging.Formatter(
                    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
                logger.addHandler(handler)
            elif loggers == 'asyncio':
                self.loop.set_debug(True)
                asynciologger = logging.getLogger('asyncio')
                asynciologger.setLevel(logging.DEBUG)
                asynciologgerhandler = logging.FileHandler(
                    filename=os.path.join(
                        sys.path[0], 'resources', 'Logs', 'asyncio.log'),
                        encoding='utf-8', mode='w')
                asynciologgerhandler.setFormatter(logging.Formatter(
                    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
                asynciologger.addHandler(asynciologgerhandler)

    def set_up_discord_logger(self):
        """
        Sets up the Discord Logger.
        """
        self.set_up_loggers(loggers='discord')

    def set_up_asyncio_logger(self):
        """
        Sets up the asyncio Logger.
        """
        self.set_up_loggers(loggers='asyncio')

    # Helpers.

    def login_helper(self):
        """
        Bot Login Helper.
        """
        while True:
            ret = self.login_info()
            if ret is not None and ret is not -1:
                break

    # Login stuff.

    def login_info(self):
        """
        Allows the bot to Connect / Reconnect.
        :return: Nothing or -1/-2 on failure.
        """
        if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
            try:
                if self.BotConfig.bot_token is not None:
                    self.is_bot_logged_in = True
                    self.loop.run_until_complete(self.start(
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
                    return -2
            except TypeError:
                pass
            except KeyboardInterrupt:
                pass
            except asyncio.futures.InvalidStateError:
                return self._rec.reconnect_helper()
            except aiohttp.ClientResponseError:
                return self._rec.reconnect_helper()
            except aiohttp.ClientOSError:
                return self._rec.reconnect_helper()
            except RuntimeError:
                self.http.recreate()
            if self.is_bot_logged_in:
                if not self.is_logged_in:
                    pass
                else:
                    return self._rec.reconnect_helper()
        else:
            print(str(self.consoletext['Credentials_Not_Found'][0]))
            return -2

    def variable(self):
        """
        Function that makes Certain things on the
        on_ready event only happen 1
        time only. (e.g. the logged in printing stuff)
        """
        if not BotClient.logged_in:
            BotClient.logged_in = True
            self.logged_in_ = True


def main():
    """
    EntryPoint to DecoraterBot.
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
