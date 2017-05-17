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


def construct_reply(message):
    """
    Constructs an bot reply.
    """
    msginfo = 'Missing the Send Message Permissions in the '
    msginfo += message.server.name + ' server on the '
    msginfo += message.channel.name + ' channel.'
    return msginfo


class BotPMError:
    """
    Class for PMing bot errors.
    """
    def __init__(self, bot):
        self.bot = bot

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
                content=construct_reply(message))
        except discord.errors.Forbidden:
            return
