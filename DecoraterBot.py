# coding=utf-8
"""
    DecoraterBot's source is protected by Cheese.lab industries Inc. Even though it is Open Source
    any and all users waive the right to say that this bot's code was stolen when it really was not.
    Me @Decorater the only core developer of this bot do not take kindly to those false Allegations.
    it would piss any DEVELOPER OFF WHEN THEY SPEND ABOUT A YEAR CODING STUFF FROM SCRATCH AND THEN BE ACCUSED OF SHIT LIKE THIS.
    
    So, do not do it. If you do Cheese.lab Industries Inc. Can and Will do after you for such cliams that it deems untrue.
    
    Cheese.lab industries Inc. Belieces in the rights of Original Developers of bots. They do not take kindly to BULLSHIT.
    
    Any and all Developers work all the time, many of them do not get paid for their hard work.
    
    I am one of those who did not get paid even though I am the original Developer I coded this bot from the bottom with no lines of code at all.
    
    And how much money did I get from it for my 11 months or so of working on it? None- yeah thats right 0$ how pissed can someone be?
    Exactly I have over stretched my relatives money that they paid for Internet and power for my computer so that way I can code my bot.
    
    However shit does go out of the Fan with a possible 600$ or more that my Laptop Drastically needs to Repairs as it is 10 years old and is falling apart
    
    I am half tempted myself to pulling this bot from github and making it on patrion that boobot is also on to help me with my development needs.
    
    So, as such I accept issue requests, but please do not give me bullshit I hate it as it makes everything worse than the way it is.
    
    You do have the right however to:
        -> Contribute to the bot's development.
        -> fix bugs.
        -> add commands.
        -> help finish the per server config (has issues)
        -> update the Voice commands to be better (and not use globals which is 1 big thing that kilsl it).

    But keep in mind any and all Changes you make can and will be property of Cheese.lab Induestries Inc.
"""
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
