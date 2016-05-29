# coding=utf-8
import discord
import asyncio
import io
import sys
import subprocess
import os
import traceback
from discord.ext import commands

async def _resolve_send_message_error(client, message):
    unabletosendmessageerror_01 = 'Missing the Send Message Permssions in the '
    unabletosendmessageerror_02 = message.channel.server.name
    unabletosendmessageerror_03 = ' server on the ' + message.channel.name + ' channel.'
    unabletosendmessageerror_fix = unabletosendmessageerror_01 + unabletosendmessageerror_02
    unabletosendmessageerror = unabletosendmessageerror_fix + unabletosendmessageerror_03
    try:
        await client.send_message(message.channel.server.owner, unabletosendmessageerror)
    except discord.errors.Forbidden:
        # Well the Bot was blocked by the user. This is to Handle it so it dont traceback.
        return

async def _resolve_unloaded_commands_error(client, message):
    try:
        msgdata = 'Sorry, Commands was unloaded by owner for now '
        message_data = msgdata + '(He might be updating them).'
        await client.send_message(message.channel, message_data)
    except discord.errors.Forbidden:
        _resolve_send_message_error(client, message)


# Taskkill cleanup of ffmpeg.exe
# noinspection PyUnusedLocal
def ffm_cleanup(client, message):
    cmd = 'taskkill /T /F /IM "ffmpeg.exe"'
    logfile = sys.path[0] + '\\resources\\Logs\\taskkill_log.txt'
    taskkilloutput = io.open(logfile, 'w', encoding='utf-8')
    subprocess.Popen(cmd, shell=True, stdout=taskkilloutput, stderr=taskkilloutput)
    taskkilloutput.close()
