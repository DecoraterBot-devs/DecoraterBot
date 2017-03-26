# coding=utf-8
"""
Webhooks plugin for DecoraterBot.
"""

import discord
from discord.ext import commands
from discord_webhooks import *


class WebHooks:
    """
    Webhook Commands Extension.
    """
    def __init__(self, bot):
        self.bot = bot
        self.webhook_class = Webhook(self.bot)
        self.request_webhook = self.webhook_class.request_webhook

    def botcommand(self):
        """Stores all command names in a dictionary."""
        self.bot.commands_list.append('sendtext')
        self.bot.commands_list.append('sendimages')
        self.bot.commands_list.append('sendannouncement')

    def __unload(self):
        """
        Clears registered commands.
        """
        self.bot.commands_list.remove('sendtext')
        self.bot.commands_list.remove('sendimages')
        self.bot.commands_list.remove('sendannouncement')

    @commands.command(name='sendtext', pass_context=True, no_pm=True)
    async def webhooktext_command(self, ctx):
        """
        ::sendtext request command for DecoraterBot.
        """
        msgdata = ctx.message.content[len(ctx.prefix + "sendtext"):].strip()
        # if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
        #     return
        role2 = discord.utils.find(lambda role: role.name == 'Webhook Manager',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            if ctx.message.server.id == '273134655702827008':
                await self.request_webhook(
                    '/284510404162355200/F2CFGqlX9UpC_hRpLIbFLzTnXncgqFdaLz'
                    '09fOI92fihzfQT6lT0VB2ZjW4FtEZPcurS',
                    content=msgdata)
        else:
            await self.bot.send_message(
                ctx.message.channel,
                'Sorry, you do not have the ``Webhook Manager`` role to use '
                'this command.')

    @commands.command(name='sendimages', pass_context=True, no_pm=True)
    async def webhookimages_command(self, ctx):
        """
        ::sendimages request command for DecoraterBot.
        """
        # if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
        #     return
        role2 = discord.utils.find(lambda role: role.name == 'Webhook Manager',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            if ctx.message.server.id == '273134655702827008':
                file = open(
                    '{0}{1}resources{1}images{1}other{1}image.jpg'.format(
                        self.bot.path, self.bot.sepa), 'rb')
                data = file.read()
                await self.request_webhook(
                    '/284510404162355200/F2CFGqlX9UpC_hRpLIbFLzTnXncgqFdaLz'
                    '09fOI92fihzfQT6lT0VB2ZjW4FtEZPcurS',
                    file=data)
        else:
            await self.bot.send_message(
                ctx.message.channel,
                'Sorry, you do not have the ``Webhook Manager`` role to use '
                'this command.')

    @commands.command(name='sendannouncement', pass_context=True, no_pm=True)
    async def webhookannouncement_command(self, ctx):
        """
        ::sendannouncement request command for DecoraterBot.
        """
        msgdata = ctx.message.content[
                  len(ctx.prefix + "sendannouncement"):].strip()
        # if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
        #     return
        role2 = discord.utils.find(lambda role: role.name == 'Webhook Manager',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            if ctx.message.server.id == '273134655702827008':
                await self.request_webhook(
                    '/294680827579727873/Op_LqGeUQiC2MgeNS-EFhbaNj1ZGH5VGH0'
                    '_5eshfdkSQYPPGo6r0RllOdHGXPrlV0XVW',
                    content=msgdata)
        else:
            await self.bot.send_message(
                ctx.message.channel,
                'Sorry, you do not have the ``Webhook Manager`` role to use '
                'this command.')


def setup(bot):
    """
    DecoraterBot's Webhook Plugin.
    """
    new_cog = WebHooks(bot)
    new_cog.botcommand()
    bot.add_cog(new_cog)
