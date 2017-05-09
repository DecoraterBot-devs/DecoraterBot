# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import traceback
from .BotErrors import CogUnloadError


__all__ = ['PluginContainer']


def get_plugin_full_name(plugin_name):
    """
    returns the plugin's full name.
    """
    if plugin_name is not None:
        return 'DecoraterBotCore.plugins.{0}'.format(
            plugin_name)
    return None


class PluginContainer:
    """
    Container class for bot cogs.
    """
    def __init__(self, bot):
        self.bot = bot

    def load_bot_extension(self, extension_full_name):
        """
        loads an bot extension module.
        """
        try:
            self.bot.load_extension(extension_full_name)
        except Exception:
            return str(traceback.format_exc())

    def unload_bot_extension(self, extension_full_name):
        """
        unloads an bot extension module.
        """
        self.bot.unload_extension(extension_full_name)

    def load_plugin(self, plugin_name):
        """
        Loads up a plugin in the plugins folder in DecoraterBotCore.
        """
        pluginfullname = get_plugin_full_name(plugin_name)
        if pluginfullname is None:
            raise ImportError(
                "Plugin Name cannot be empty.")
        err = self.load_bot_extension(pluginfullname)
        if err is not None:
            return err

    def unload_plugin(self, plugin_name):
        """
        Unloads a plugin in the plugins folder in DecoraterBotCore.
        """
        pluginfullname = get_plugin_full_name(plugin_name)
        if pluginfullname is None:
            raise CogUnloadError(
                "Plugin Name cannot be empty.")
        self.unload_bot_extension(pluginfullname)


    def reload_plugin(self, plugin_name):
        """
        Reloads a plugin in the plugins folder in DecoraterBotCore.
        """
        self.unload_plugin(plugin_name)
        err = self.load_plugin(plugin_name)
        if err is not None:
            return err
