# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import discord

__all__ = ['BotPMError']


class BotPMError:
    """
    Class for PMing bot errors.
    """
    def __init__(self, bot):
        self.bot = bot

    def construct_reply(self, message):
        """Constructs an bot reply."""
        svr_name = message.channel.server.name
        cnl_name = message.channel.name
        msginfo = 'Missing the Send Message Permssions in the ' \
                  '{0} server on the {1} channel.'
        unabletosendmessageerror = msginfo.format(svr_name, cnl_name)
        return unabletosendmessageerror

    async def resolve_send_message_error(self, ctx):
        """
        Relolves Errors when Sending messages.
        :param ctx: Merssage Context.
        :return: Nothing.
        """
        await self.resolve_send_message_error_old(
            ctx.message)

    async def resolve_send_message_error_old(self, message):
        """
        Relolves Errors when Sending messages.
        :param message: Merssage.
        :return: Nothing.
        """
        unabletosendmessageerror = self.construct_reply(
            message)
        try:
            await bot.send_message(
                message.author,
                content=unabletosendmessageerror)
        except discord.errors.Forbidden:
            return
