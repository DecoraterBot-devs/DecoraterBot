# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import discord

__all__ = ['resolve_send_message_error', 'resolve_send_message_error_old']


def construct_reply(message):
    """Constructs an bot reply."""
    svr_name = message.channel.server.name
    cnl_name = message.channel.name
    msginfo = 'Missing the Send Message Permssions in the ' \
              '{0} server on the {1} channel.'
    unabletosendmessageerror = msginfo.format(svr_name, cnl_name)
    return unabletosendmessageerror


async def resolve_send_message_error(bot, ctx):
    """
    Relolves Errors when Sending messages.
    :param bot: Discord Client.
    :param ctx: Merssage Context.
    :return: Nothing.
    """
    unabletosendmessageerror = construct_reply(ctx.message)
    try:
        await bot.send_message(ctx.message.author,
                               content=unabletosendmessageerror)
    except discord.errors.Forbidden:
        return


async def resolve_send_message_error_old(bot, message):
    """
    Relolves Errors when Sending messages.
    :param bot: Discord Client.
    :param message: Merssage.
    :return: Nothing.
    """
    unabletosendmessageerror = construct_reply(ctx.message)
    try:
        await bot.send_message(message.author,
                               content=unabletosendmessageerror)
    except discord.errors.Forbidden:
        return
