# coding=utf-8
import os
import discord
import io
import ctypes
import asyncio

version = 'v1.0.0.3'
client = discord.Client()


def changewindowtitle():
    ctypes.windll.kernel32.SetConsoleTitleW("Decorater " + version)


@client.event
async def commands(client, message):
    if message.channel.is_private is not False:
        return
    else:
        if message.content.lower() == 'f':
            await client.send_message(message.channel, message.author.name + " has paid their respects! :eggplant:")
        else:
            return
        if message.content.startswith(client.user.mention):
            raw_content = message.content.strip(client.user.mention)
            if raw_content == ' clear':
                if message.author.id == client.user.id:
                    async for msg in client.logs_from(message.channel, limit=100):
                        if msg.author.id == client.user.id:
                            try:
                                await client.delete_message(msg)
                            except discord.HTTPException:
                                return
                else:
                    message_data = ' does not have permissions to use this command.'
                    await client.send_message(message.channel, message.author.name + message_data)
            else:
                return
#    if message.content.startswith('::open'):
#        os.startfile(".\DecoraterBot.bat")
#        await client.logout()
#    return
