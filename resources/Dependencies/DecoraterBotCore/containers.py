# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import traceback

__all__ = ['load_plugin', 'unload_plugin', 'reload_plugin',
           'load_command', 'unload_command', 'reload_command']


def get_plugin_full_name(plugin_name):
    """
    returns the plugin's full name.
    """
    return 'DecoraterBotCore.plugins.{0}'.format(plugin_name)


def get_command_full_name(command_name):
    """
    returns the command's full name.
    """
    return 'DecoraterBotCore.commands.{0}'.format(command_name)


def load_bot_extension(bot, extension_full_name):
    """
    loads an bot extension module.
    """
    try:
        bot.load_extension(extension_full_name)
    except Exception:
        return str(traceback.format_exc())


def unload_bot_extension(bot, extension_full_name):
    """
    unloads an bot extension module.
    """
    bot.unload_extension(extension_full_name)


def load_plugin(bot, plugin_name):
    """
    Loads up a plugin in the plugins folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param plugin_name: the name of the plugin to load.
    :returns: Nothing but loaded plugin or Traceback of Error.
    """
    pluginfullname = get_plugin_full_name(plugin_name)
    err = load_bot_extension(bot, pluginfullname)
    if err is not None:
        return err


def unload_plugin(bot, plugin_name):
    """
    Unloads a plugin in the plugins folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param plugin_name: the name of the plugin to unload.
    :returns: Nothing but unloaded plugin.
    """
    pluginfullname = get_plugin_full_name(plugin_name)
    unload_bot_extension(bot, pluginfullname)


def reload_plugin(bot, plugin_name):
    """
    Reloads a plugin in the plugins folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param plugin_name: the name of the plugin to reload.
    :returns: Nothing but reloaded plugin.
    """
    unload_plugin(bot, plugin_name)
    err = load_plugin(bot, plugin_name)
    if err is not None:
        return err


def load_command(bot, command_name):
    """
    Loads up a plugin in the commands folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param command_name: the name of the plugin to load.
    :returns: Nothing but loaded plugin or Traceback of Error.
    """
    commandsfullname = get_command_full_name(command_name)
    err = load_bot_extension(bot, commandsfullname)
    if err is not None:
        return err


def unload_command(bot, command_name):
    """
    Unloads a plugin in the commands folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param command_name: the name of the plugin to unload.
    :returns: Nothing but unloaded plugin.
    """
    commandsfullname = get_command_full_name(command_name)
    unload_bot_extension(bot, commandsfullname)


def reload_command(bot, command_name):
    """
    Reloads a plugin in the commands folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param command_name: the name of the plugin to reload.
    :returns: Nothing but reloaded plugin.
    """
    unload_command(bot, command_name)
    err = load_command(bot, command_name)
    if err is not None:
        return err
