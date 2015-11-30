import os
import DecoraterBotCore
from requests.certs import where
import sys
import os.path
import discord

PATH='.\login.ini'
where()
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.executable), "cacert.pem")

client = discord.Client()
DecoraterBotCore.Core.changeWindowTitle()

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.readfp(open(PATH))
    discord_user_email = config.get("login", "email")
    discord_user_password = config.get("login", "password")
    discord_user_id = config.get("login", "userid")
    client.login(discord_user_email, discord_user_password)
else:
    discord_user_email = 'email'
    discord_user_password = 'password'
    discord_user_id = 'user_id'
    client.login(discord_user_email, discord_user_password)
@client.event
def on_message(message):
    DecoraterBotCore.Core.commands(client, message)

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    client.send_message(discord.Object(id='93740277918871552'), "**DecoraterBot Status: Online**")
#    client.send_message(discord.Object(id='110374132432011264'), "**DecoraterBot Status: Online**")
    client.send_message(discord.Object(id='118098998744580098'), "**DecoraterBot Status: Online**")
    client.send_message(discord.Object(id='81392063312044032'), "**DecoraterBot Status: Online**")

client.run()

@client.event
def on_error(event, *args, **kwargs):
    DecoraterBotCore.Core.on_error(event, *args, **kwargs)
