# coding=utf-8
import os
import sys
sys.dont_write_bytecode = True
try:
    import discord
except ImportError:
    appendpath = sys.path[0] + "\\resources\\Dependencies"
    sys.path.append(appendpath)
    import discord
import DecoraterBotCore
import asyncio

DecoraterBotCore.Core.BotCore._asyncio_logger()
DecoraterBotCore.Core.BotCore._discord_logger()
client = discord.Client()
DecoraterBotCore.Core.BotCore.changewindowtitle()
# DecoraterBotCore.Core.BotCore.changewindowsize()


@client.async_event
def on_message(message):
    yield from DecoraterBotCore.Core.BotCore.commands(client, message)


@client.async_event
def on_message_delete(message):
    yield from DecoraterBotCore.Core.BotCore.deletemessage(client, message)


@client.async_event
def on_message_edit(before, after):
    yield from DecoraterBotCore.Core.BotCore.editmessage(client, before, after)


@client.async_event
def on_channel_delete(channel):
    yield from DecoraterBotCore.Core.BotCore.channeldelete(channel)


@client.async_event
def on_channel_create(channel):
    yield from DecoraterBotCore.Core.BotCore.channelcreate(channel)


@client.async_event
def on_channel_update(before, after):
    yield from DecoraterBotCore.Core.BotCore.channelupdate(before, after)


@client.async_event
def on_member_ban(member):
    yield from DecoraterBotCore.Core.BotCore.memberban(client, member)


@client.async_event
def on_member_unban(server, user):
    yield from DecoraterBotCore.Core.BotCore.memberunban(server, user)


@client.async_event
def on_member_remove(member):
    yield from DecoraterBotCore.Core.BotCore.memberremove(client, member)


@client.async_event
def on_member_update(before, after):
    yield from DecoraterBotCore.Core.BotCore.memberupdate(before, after)


@client.async_event
def on_member_join(member):
    yield from DecoraterBotCore.Core.BotCore.memberjoin(client, member)


@client.async_event
def on_server_available(server):
    yield from DecoraterBotCore.Core.BotCore._server_available(server)


@client.async_event
def on_server_unavailable(server):
    yield from DecoraterBotCore.Core.BotCore._server_unavailable(server)


@client.async_event
def on_server_join(server):
    yield from DecoraterBotCore.Core.BotCore.serverjoin(server)


@client.async_event
def on_server_remove(server):
    yield from DecoraterBotCore.Core.BotCore.serverremove(server)


@client.async_event
def on_server_update(before, after):
    yield from DecoraterBotCore.Core.BotCore.serverupdate(before, after)


@client.async_event
def on_server_role_create(role):
    yield from DecoraterBotCore.Core.BotCore.serverrolecreate(role)


@client.async_event
def on_server_role_delete(role):
    yield from DecoraterBotCore.Core.BotCore.serverroledelete(role)


@client.async_event
def on_server_role_update(before, after):
    yield from DecoraterBotCore.Core.BotCore.serverroleupdate(before, after)


@client.async_event
def on_group_join(channel, user):
    yield from DecoraterBotCore.Core.BotCore.groupjoin(channel, user)


@client.async_event
def on_group_remove(channel, user):
    yield from DecoraterBotCore.Core.BotCore.groupremove(channel, user)


@client.async_event
def on_error(event, *args, **kwargs):
    yield from DecoraterBotCore.Core.BotCore.errors(event, *args, **kwargs)


@client.async_event
def on_voice_state_update(before, after):
    yield from DecoraterBotCore.Core.BotCore.voiceupdate(before, after)


@client.async_event
def on_typing(channel, user, when):
    yield from DecoraterBotCore.Core.BotCore.typing(channel, user, when)


@client.async_event
def on_socket_raw_receive(msg):
    yield from DecoraterBotCore.Core.BotCore.raw_recv(msg)


@client.async_event
def on_socket_raw_send(payload):
    yield from DecoraterBotCore.Core.BotCore.raw_send(payload)


@client.async_event
def on_ready():
    yield from DecoraterBotCore.Core.BotCore._bot_ready(client)


@client.async_event
def on_resumed():
    yield from DecoraterBotCore.Core.BotCore._bot_resumed()


DecoraterBotCore.Core.BotCore._login_helper(client)
