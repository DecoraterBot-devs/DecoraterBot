# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import discord

__all__ = ['BotPMError', 'construct_reply']


def construct_reply(message, msgdata):
    """
    Constructs an bot reply.
    """
    return msgdata % (message.server.name, message.channel.name)


class BotPMError:
    """
    Class for PMing bot errors.
    """
    def __init__(self, bot):
        self.bot = bot
        self.error_text = self.bot.PluginConfigReader(
            file='ConsoleWindow.json')
        self.error_text = self.error_text[
            self.bot.BotConfig.language]

    async def resolve_send_message_error(self, ctx):
        """
        Resolves errors when sending messages.
        """
        await self.resolve_send_message_error_old(
            ctx.message)

    async def resolve_send_message_error_old(self, message):
        """
        Resolves errors when sending messages.
        """
        try:
            await self.bot.send_message(
                message.author,
                content=construct_reply(
                    message, self.error_text['error_message'][0]))
        except discord.errors.Forbidden:
            return
