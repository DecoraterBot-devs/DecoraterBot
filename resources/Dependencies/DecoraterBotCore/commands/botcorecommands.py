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
import time
import discord
from discord.ext import commands
from sasync import *
from .. import BotPMError
from .. import containers


class BotCoreCommands:
    """
    Class for Commands in this in this Core Module file.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='uptime', pass_context=True, no_pm=False)
    @async
    def uptime_command(self, ctx):
        """
        Command.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            stop = time.time()
            seconds = stop - self.bot.start
            days = int(((seconds / 60) / 60) / 24)
            hours = str(int((seconds / 60) / 60 - (days * 24)))
            minutes = str(int((seconds / 60) % 60))
            seconds = str(int(seconds % 60))
            days = str(days)
            time_001 = str(self.bot.botmessages['Uptime_command_data'][0]).format(days, hours, minutes, seconds)
            time_parse = time_001
            try:
                yield from self.bot.send_message(ctx.message.channel, content=time_parse)
            except discord.errors.Forbidden:
                return

    @commands.command(name='reload', pass_context=True, no_pm=True)
    @async
    def reload_commands_command(self, ctx):
        """
        Command.
        """
        if ctx.message.author.id == self.bot.discord_user_id:
            desmod_new = ctx.message.content.lower()[len(self.bot.bot_prefix + 'reload '):].strip()
            self.bot._somebool = False
            ret = ""
            if desmod_new is not None:
                self.bot._somebool = True
                ret = containers.reload_command(self.bot, desmod_new)
            if self.bot._somebool is True:
                if ret is not None:
                    try:
                        reload_data = str(self.bot.botmessages['reload_command_data'][1]).format(
                            ret)
                        yield from self.bot.send_message(ctx.message.channel, content=reload_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                else:
                    try:
                        msgdata = str(self.bot.botmessages['reload_command_data'][0])
                        message_data = msgdata + ' Reloaded ' + desmod_new + '.'
                        yield from self.bot.send_message(ctx.message.channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
            else:
                try:
                    yield from self.bot.send_message(ctx.message.channel,
                                                     content=str(self.bot.botmessages['reload_command_data'][2]))
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(self.bot, ctx)
        else:
            try:
                yield from self.bot.send_message(ctx.message.channel,
                                                 content=str(self.bot.botmessages['reload_command_data'][3]))
            except discord.errors.Forbidden:
                yield from BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='loadplugin', pass_context=True, no_pm=True)
    @async
    def load_plugin_command(self, ctx):
        """
        Command.
        """
        if ctx.message.author.id == self.bot.discord_user_id:
            desmod_new = ctx.message.content.lower()[len(self.bot.bot_prefix + 'loadplugin '):].strip()
            self.bot._somebool = False
            ret = ""
            if desmod_new is not None:
                self.bot._somebool = True
                ret = containers.load_plugin(self.bot, desmod_new)
            if self.bot._somebool is True:
                if ret is not None:
                    try:
                        reload_data = str(self.bot.botmessages['reload_command_data'][1]).format(
                            ret).replace('Reloading', 'Loading Plugin')
                        yield from self.bot.send_message(ctx.message.channel, content=reload_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
                else:
                    try:
                        msgdata = str(self.bot.botmessages['reload_command_data'][0])
                        message_data = msgdata + ' Loaded ' + desmod_new + '.'
                        yield from self.bot.send_message(ctx.message.channel, content=message_data)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error(self.bot, ctx)
            else:
                try:
                    yield from self.bot.send_message(ctx.message.channel,
                                                     content=str(self.bot.botmessages['reload_command_data'][2]))
                except discord.errors.Forbidden:
                    yield from BotPMError.resolve_send_message_error(self.bot, ctx)
        else:
            try:
                yield from self.bot.send_message(ctx.message.channel,
                                                 content=str(self.bot.botmessages['reload_command_data'][3]))
            except discord.errors.Forbidden:
                yield from BotPMError.resolve_send_message_error(self.bot, ctx)


def setup(bot):
    """
    Sets up these commands.
    :param bot: Bot client.
    :return: Nothing really.
    """
    bot.add_cog(BotCoreCommands(bot))
