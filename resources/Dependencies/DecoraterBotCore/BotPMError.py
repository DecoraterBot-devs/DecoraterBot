# coding=utf-8
import discord
import asyncio
import io
import sys
import subprocess
import os
import traceback
from discord.ext import commands


@asyncio.coroutine
def _resolve_send_message_error(client, message):
    svr_name = message.channel.server.name
    cnl_name = message.channel.name
    msginfo = 'Missing the Send Message Permssions in the {0} server on the {1} channel.'
    unabletosendmessageerror = msginfo.format(svr_name, cnl_name)
    try:
        yield from client.send_message(message.channel.server.owner, unabletosendmessageerror)
    except discord.errors.Forbidden:
        return


@asyncio.coroutine
def _resolve_unloaded_commands_error(client, message):
    msgdata = 'Sorry, Commands was unloaded by my owner for now (He might be updating them).'
    try:
        yield from client.send_message(message.channel, msgdata)
    except discord.errors.Forbidden:
        _resolve_send_message_error(client, message)
