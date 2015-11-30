import os
import discord
import DecoraterCore
import sys
import os.path
import ctypes
from requests.certs import where


PATH='.\login.ini'
where()
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.executable), "cacert.pem")

client = discord.Client()
DecoraterCore.Core.changeWindowTitle()

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.readfp(open(PATH))
    discord_user_email = config.get("login2", "email")
    discord_user_password = config.get("login2", "password")
    discord_user_id = config.get("login2", "userid")
    client.login(discord_user_email, discord_user_password)
else:
    discord_user_email = 'email'
    discord_user_password = 'password'
    discord_user_id = 'user_id'
    client.login(discord_user_email, discord_user_password)

@client.event
def on_message(message):
    DecoraterCore.Core.commands(client, message)

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()
