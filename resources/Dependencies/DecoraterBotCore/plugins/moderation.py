# coding=utf-8
"""
moderation plugin for DecoraterBot.
"""
import regex

import discord
from discord.ext import commands


# This module's commands are so buggy they do not work right now.
# I would like it if someone would help me fix them and pull
# request the fixtures to this file to make them work.
# Also I plan to make my own commands register for the bot to register
# all commands to get an easy list for some features to not bug out
# because it does not know all the commands the bot has.


class ModerationCommands:
    """
    Moderation Commands Extension to the
        default DecoraterBot Moderation commands.
    """
    def __init__(self, bot):
        self.sent_prune_error_message = False
        self.bot = bot

    def botcommand(self):
        """Stores all command names in a dictionary."""
        self.bot.commands_list.append('ban')
        self.bot.commands_list.append('softban')
        self.bot.commands_list.append('kick')
        self.bot.commands_list.append('prune')
        self.bot.commands_list.append('clear')
        self.bot.commands_list.append('warn')
        self.bot.commands_list.append('mute')

    def __unload(self):
        """
        Clears registered commands.
        """
        self.bot.commands_list.remove('ban')
        self.bot.commands_list.remove('softban')
        self.bot.commands_list.remove('kick')
        self.bot.commands_list.remove('prune')
        self.bot.commands_list.remove('clear')
        self.bot.commands_list.remove('warn')
        self.bot.commands_list.remove('mute')

    @commands.command(name='ban', pass_context=True, no_pm=True)
    async def ban_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            for disuser in ctx.message.mentions:
                listdata = ctx.message.channel.server.members
                member2 = discord.utils.find(
                    lambda member: member.name == disuser.name, listdata)
                try:
                    await self.bot.ban(member2, delete_message_days=7)
                    try:
                        message_data = str(
                            self.bot.botmessages['ban_command_data'][
                                0]).format(member2)
                        await self.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                except discord.Forbidden:
                    try:
                        await self.bot.send_message(ctx.message.channel,
                                                    content=str(
                                                        self.bot.botmessages[
                                                            'ban_command_data'
                                                        ][1]))
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                except discord.HTTPException:
                    try:
                        await self.bot.send_message(ctx.message.channel,
                                                    content=str(
                                                        self.bot.botmessages[
                                                            'ban_command_data'
                                                        ][2]))
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                break
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.bot.botmessages[
                                                        'ban_command_data'
                                                    ][3]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(self.bot.botmessages[
                                                            'ban_command_data'
                                                        ][4]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot,
                                                                     ctx)

    @commands.command(name='softban', pass_context=True, no_pm=True)
    async def softban_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            for disuser in ctx.message.mentions:
                memberlist = ctx.message.channel.server.members
                member2 = discord.utils.find(
                    lambda member: member.name == disuser.name, memberlist)
                try:
                    await self.bot.ban(member2, delete_message_days=7)
                    await self.bot.unban(member2.server, member2)
                    try:
                        message_data = str(
                            self.bot.botmessages['softban_command_data'][
                                0]).format(member2)
                        await self.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                except discord.Forbidden:
                    try:
                        msg_data = str(
                            self.bot.botmessages['softban_command_data'][1])
                        await self.bot.send_message(ctx.message.channel,
                                                    content=msg_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                except discord.HTTPException:
                    try:
                        msg_data = str(
                            self.bot.botmessages['softban_command_data'][2])
                        await self.bot.send_message(ctx.message.channel,
                                                    content=msg_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                break
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.bot.botmessages[
                                                        'softban_command_data'
                                                    ][3]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(
                                                self.bot.botmessages[
                                                    'softban_command_data'
                                                ][4]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot,
                                                                     ctx)

    @commands.command(name='kick', pass_context=True, no_pm=True)
    async def kick_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            for disuser in ctx.message.mentions:
                memberlist = ctx.message.channel.server.members
                member2 = discord.utils.find(
                    lambda member: member.name == disuser.name, memberlist)
                try:
                    await self.bot.kick(member2)
                    try:
                        message_data = str(
                            self.bot.botmessages['kick_command_data'][
                                0]).format(member2)
                        await self.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                except discord.Forbidden:
                    try:
                        await self.bot.send_message(ctx.message.channel,
                                                    content=str(
                                                        self.bot.botmessages[
                                                            'kick_command_data'
                                                        ][1]))
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                except discord.HTTPException:
                    try:
                        await self.bot.send_message(ctx.message.channel,
                                                    content=str(
                                                        self.bot.botmessages[
                                                            'kick_command_data'
                                                        ][2]))
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                break
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.bot.botmessages[
                                                        'kick_command_data'][
                                                        3]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(self.bot.botmessages[
                                                            'kick_command_data'
                                                        ][4]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot,
                                                                     ctx)

    @commands.command(name='prune', pass_context=True, no_pm=True)
    async def prune_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            if self.sent_prune_error_message:
                self.sent_prune_error_message = False
            role2 = discord.utils.find(
                lambda role: role.name == 'Bot Commander',
                ctx.message.channel.server.roles)
            """
            if ctx.message.author.id == owner_id:
                opt = ctx.message.content[len(_bot_prefix + "prune "):].strip()
                num = 1
                if opt:
                    try:
                        num = int(opt)
                    except:
                        return
                await self.prune_command_iterater_helper(ctx, num)
            else:
            """
            if role2 in ctx.message.author.roles:
                opt = ctx.message.content[
                      len(ctx.prefix + "prune "):].strip()
                num = 1
                if opt:
                    try:
                        num = int(opt)
                    except Exception as e:
                        str(e)
                        return
                await self.prune_command_iterater_helper(ctx, num)
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.bot.botmessages[
                                                        'prune_command_data'][
                                                        1]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)

    @commands.command(name='clear', pass_context=True, no_pm=True)
    async def clear_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            await self.clear_command_iterater_helper(ctx)

    @commands.command(name='warn', pass_context=True)
    async def warn_command(self, ctx):
        """
        ::warn Command for DecoraterBot.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            match = regex.match('warn[ ]+(<@(.+?)>[ ])+(.+)',
                                ctx.message.content[len(ctx.prefix):].strip())
            if match:
                warning = match.captures(3)[0]
                targets = match.captures(2)
                for target in targets:
                    await self.bot.send_message(target, content=warning)

    @commands.command(name='mute', pass_context=True)
    async def mute_command(self, ctx):
        """
        ::mute Search Command for DecoraterBot.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            match = regex.match(ctx.prefix + 'mute[ ]+(<@(.+?)>[ ])+(.+)',
                                ctx.message.content)
            if match:
                mute_time = match.captures(3)[0]
                # targets = match.captures(2)
                if mute_time is not None:
                    # s = seconds
                    # m = minutes
                    # h = hours
                    # d = days
                    # w = weeks
                    # M = months
                    # y = years
                    pattern = '(\d+)(s|m|h|d|w|M|y)'
                    searchres = regex.match(pattern, mute_time)
                    if searchres is not None:
                        # TODO: Finish this command.
                        return

    # Helpers.

    async def prune_command_iterater_helper(self, ctx, num):
        """
        Prunes Messages.
        :param self:
        :param ctx: Message Context.
        :param num:
        :return: Nothing.
        """
        # messages = []
        # async for message in self.bot.logs_from(ctx.message.channel,
        #                                         limit=num + 1):
        #     messages.append(message)
        # for message in messages:
        #     try:
        #         await self.bot.delete_message(message)
        try:
            await self.bot.purge_from(ctx.message.channel, limit=num + 1)
        except discord.HTTPException:
            if self.sent_prune_error_message is False:
                self.sent_prune_error_message = True
                await self.bot.send_message(ctx.message.channel,
                                            content=str(
                                                self.bot.botmessages[
                                                    'prune_command_data'][0]))
            else:
                return

    async def clear_command_iterater_helper(self, ctx):
        """
        Clears the bot's messages.
        :param self:
        :param ctx: Message Context.
        :return: Nothing.
        """

        try:
            await self.bot.purge_from(ctx.message.channel, limit=100,
                                      check=lambda e: e.author == (
                                                      ctx.message.server.me))
        except discord.HTTPException:
            return


def setup(bot):
    """
    DecoraterBot's Moderation Plugin.
    """
    new_cog = ModerationCommands(bot)
    new_cog.botcommand()
    bot.add_cog(new_cog)
