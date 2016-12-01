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
import traceback

__all__ = ['load_plugin', 'unload_plugin', 'reload_plugin',
           'load_command', 'unload_command', 'reload_command']


def load_plugin(bot, plugin_name):
    """
    Loads up a plugin in the plugins folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param plugin_name: the name of the plugin to load.
    :returns: Nothing but loaded plugin or Traceback of Error.
    """
    pluginfullname = 'DecoraterBotCore.plugins.{0}'.format(plugin_name)
    try:
        bot.load_extension(pluginfullname)
    except Exception as e:
        str(e)
        return str(traceback.format_exc())


def unload_plugin(bot, plugin_name):
    """
    Unloads a plugin in the plugins folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param plugin_name: the name of the plugin to unload.
    :returns: Nothing but unloaded plugin.
    """
    pluginfullname = 'DecoraterBotCore.plugins.{0}'.format(plugin_name)
    bot.unload_extension(pluginfullname)


def reload_plugin(bot, plugin_name):
    """
    Reloads a plugin in the plugins folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param plugin_name: the name of the plugin to reload.
    :returns: Nothing but reloaded plugin.
    """
    pluginfullname = 'DecoraterBotCore.plugins.{0}'.format(plugin_name)
    unload_plugin(bot, plugin_name)
    try:
        bot.load_extension(pluginfullname)
    except Exception as e:
        str(e)
        return str(traceback.format_exc())


def load_command(bot, command_name):
    """
    Loads up a plugin in the commands folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param command_name: the name of the plugin to load.
    :returns: Nothing but loaded plugin or Traceback of Error.
    """
    commandsfullname = 'DecoraterBotCore.commands.{0}'.format(command_name)
    try:
        bot.load_extension(commandsfullname)
    except Exception as e:
        str(e)
        return str(traceback.format_exc())


def unload_command(bot, command_name):
    """
    Unloads a plugin in the commands folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param command_name: the name of the plugin to unload.
    :returns: Nothing but unloaded plugin.
    """
    commandsfullname = 'DecoraterBotCore.commands.{0}'.format(command_name)
    bot.unload_extension(commandsfullname)


def reload_command(bot, command_name):
    """
    Reloads a plugin in the commands folder in DecoraterBotCore.
    :param bot: Bot client from the Commands Extension.
    :param command_name: the name of the plugin to reload.
    :returns: Nothing but reloaded plugin.
    """
    commandsfullname = 'DecoraterBotCore.commands.{0}'.format(command_name)
    unload_command(bot, command_name)
    try:
        bot.load_extension(commandsfullname)
    except Exception as e:
        str(e)
        return str(traceback.format_exc())
