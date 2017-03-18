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
