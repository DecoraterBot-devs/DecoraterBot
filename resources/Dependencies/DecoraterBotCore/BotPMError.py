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
    unabletosendmessageerror = 'Missing the Send Message Permssions in the {0} server on the {1} channel.'.format(message.channel.server.name, message.channel.name)
    try:
        yield from client.send_message(message.channel.server.owner, unabletosendmessageerror)
    except discord.errors.Forbidden:
        return

@asyncio.coroutine
def _resolve_unloaded_commands_error(client, message):
    msgdata = 'Sorry, Commands was unloaded by owner for now (He might be updating them).'
    try:
        yield from client.send_message(message.channel, message_data)
    except discord.errors.Forbidden:
        _resolve_send_message_error(client, message)
