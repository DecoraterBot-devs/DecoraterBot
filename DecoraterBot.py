#coding=utf-8
import os
import DecoraterBotCore
from requests.certs import where
import sys
import os.path
import discord

where()
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.executable), "cacert.pem")

client = discord.Client()
DecoraterBotCore.Core.changeWindowTitle()
DecoraterBotCore.Core.changeWindowSize()
DecoraterBotCore.Logininfo.login_info(client)
DecoraterBotCore.OnLogin.variable()

@client.event
def on_message(message):
    DecoraterBotCore.Core.commands(client, message)

DecoraterBotCore.Core.on_error(on_message)

@client.event
def on_message_delete(message):
    DecoraterBotCore.Core.deletemessage(message)

@client.event
def on_message_edit(before, after):
    DecoraterBotCore.Core.editmessage(before, after)

@client.event
def on_channel_create(channel):
    DecoraterBotCore.Channels.data(client, channel)

@client.event
def on_ready():
    DecoraterBotCore.OnLogin.on_login(client)

client.run()