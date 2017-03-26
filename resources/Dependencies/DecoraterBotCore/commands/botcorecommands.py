# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import time

import discord
from discord.ext import commands


class BotCoreCommands:
    """
    Class for Commands in this in this Core Module file.
    """
    def __init__(self, bot):
        self.bot = bot

    def botcommand(self):
        """Stores all command names in a dictionary."""
        self.bot.commands_list.append('uptime')
        self.bot.commands_list.append('reload')
        self.bot.commands_list.append('loadplugin')
        self.bot.commands_list.append('unloadplugin')
        self.bot.commands_list.append('reloadplugin')

    def __unload(self):
        """
        Clears registered commands.
        """
        self.bot.commands_list.remove('uptime')
        self.bot.commands_list.remove('reload')
        self.bot.commands_list.remove('loadplugin')
        self.bot.commands_list.remove('unloadplugin')
        self.bot.commands_list.remove('reloadplugin')

    @commands.command(name='uptime', pass_context=True, no_pm=False)
    async def uptime_command(self, ctx):
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
            time_001 = str(self.bot.botmessages['Uptime_command_data'][0]
                           ).format(days, hours, minutes, seconds)
            time_parse = time_001
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=time_parse)
            except discord.errors.Forbidden:
                return

    @commands.command(name='reload', pass_context=True, no_pm=True)
    async def reload_commands_command(self, ctx):
        """
        Command.
        """
        if ctx.message.author.id == self.bot.BotConfig.discord_user_id:
            desmod_new = ctx.message.content.lower()[len(
                ctx.prefix + 'reload '):].strip()
            self.bot._somebool = False
            ret = ""
            if desmod_new is not None:
                self.bot._somebool = True
                ret = self.bot.containers.reload_command(self.bot, desmod_new)
            if self.bot._somebool is True:
                if ret is not None:
                    try:
                        reload_data = str(
                            self.bot.botmessages['reload_command_data'][1]
                        ).format(ret)
                        await self.bot.send_message(ctx.message.channel,
                                                    content=reload_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                else:
                    try:
                        msgdata = str(
                            self.bot.botmessages['reload_command_data'][0])
                        message_data = msgdata + ' Reloaded ' + desmod_new +\
                            '.'
                        await self.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.bot.botmessages[
                                                        'reload_command_data'][
                                                        2]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(
                                                self.bot.botmessages[
                                                    'reload_command_data'][3]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(
                    self.bot, ctx)

    @commands.command(name='loadplugin', pass_context=True, no_pm=True)
    async def load_plugin_command(self, ctx):
        """
        Command.
        """
        if ctx.message.author.id == self.bot.BotConfig.discord_user_id:
            desmod_new = ctx.message.content.lower()[len(
                ctx.prefix + 'loadplugin '):].strip()
            self.bot._somebool = False
            ret = ""
            if desmod_new is not None:
                self.bot._somebool = True
                ret = self.bot.containers.load_plugin(self.bot, desmod_new)
            if self.bot._somebool is True:
                if ret is not None:
                    try:
                        reload_data = str(
                            self.bot.botmessages['reload_command_data'][1]
                        ).format(ret).replace('Reloading', 'Loading Plugin')
                        await self.bot.send_message(ctx.message.channel,
                                                    content=reload_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                else:
                    try:
                        msgdata = str(
                            self.bot.botmessages['reload_command_data'][0])
                        message_data = msgdata + ' Loaded ' + desmod_new + '.'
                        await self.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.bot.botmessages[
                                                        'reload_command_data'][
                                                        2]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(
                                                self.bot.botmessages[
                                                    'reload_command_data'][3]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(
                    self.bot, ctx)

    @commands.command(name='unloadplugin', pass_context=True, no_pm=True)
    async def unload_plugin_command(self, ctx):
        """
        Command.
        """
        if ctx.message.author.id == self.bot.BotConfig.discord_user_id:
            desmod_new = ctx.message.content.lower()[len(
                ctx.prefix + 'unloadplugin '):].strip()
            self.bot._somebool = False
            ret = ""
            if desmod_new is not None:
                self.bot._somebool = True
                ret = self.bot.containers.unload_plugin(self.bot, desmod_new)
            if self.bot._somebool is True:
                if ret is not None:
                    try:
                        reload_data = str(
                            self.bot.botmessages['reload_command_data'][1]
                        ).format(ret).replace('Reloading', 'Unloading Plugin')
                        await self.bot.send_message(ctx.message.channel,
                                                    content=reload_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                else:
                    try:
                        msgdata = str(
                            self.bot.botmessages['reload_command_data'][0])
                        message_data = msgdata + ' Unloaded ' + desmod_new +\
                            '.'
                        await self.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.bot.botmessages[
                                                        'reload_command_data'][
                                                        2]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(
                                                self.bot.botmessages[
                                                    'reload_command_data'][3]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(
                    self.bot, ctx)

    @commands.command(name='reloadplugin', pass_context=True, no_pm=True)
    async def reload_plugin_command(self, ctx):
        """
        Command.
        """
        if ctx.message.author.id == self.bot.BotConfig.discord_user_id:
            desmod_new = ctx.message.content.lower()[len(
                ctx.prefix + 'reloadplugin '):].strip()
            self.bot._somebool = False
            ret = ""
            if desmod_new is not None:
                self.bot._somebool = True
                ret = self.bot.containers.unload_plugin(self.bot, desmod_new)
            if self.bot._somebool is True:
                if ret is not None:
                    try:
                        reload_data = str(
                            self.bot.botmessages['reload_command_data'][1]
                        ).format(ret).replace('Reloading', 'Reloading Plugin')
                        await self.bot.send_message(ctx.message.channel,
                                                    content=reload_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                else:
                    try:
                        msgdata = str(
                            self.bot.botmessages['reload_command_data'][0])
                        message_data = msgdata + ' Reloaded ' + desmod_new +\
                            '.'
                        await self.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
            else:
                try:
                    await self.bot.send_message(
                        ctx.message.channel, content=str(
                            self.bot.botmessages[
                                'reload_command_data'
                            ][2]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(
                                                self.bot.botmessages[
                                                    'reload_command_data'][3]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(
                    self.bot, ctx)


def setup(bot):
    """
    Sets up these commands.
    :param bot: Bot client.
    :return: Nothing really.
    """
    new_cog = BotCoreCommands(bot)
    new_cog.botcommand()
    bot.add_cog(new_cog)
