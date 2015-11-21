import os
import discord
import requests
import sys
import os.path
import ctypes
from requests.certs import where


PATH='.\login.ini'
where()
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.executable), "cacert.pem")
version = 'v1.0.0.10'
sourcelink = ' https://github.com/AraHaan/DecoraterBot/'
botcommands = 'Available commands:\n\n**--kill <lamp or cliff> <optionally mention someone>**\n**--changelog**\n**--raid <optionally mention where>**\n**--pyversion**\n**--source**'
changelog = "Created DecoraterBot.\n" + version + "\n\nChanges:\n+ Added **--source** command"

client = discord.Client()

ctypes.windll.kernel32.SetConsoleTitleA("DecoraterBot " + version)
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
    if(message.content.startswith('--kill')):
        for disuser in message.mentions:
            user = discord.utils.find(lambda member: member.name == disuser.name, message.channel.server.members)
            if "lamp" in message.content.split():
                client.send_message(message.channel, message.author.mention() + " took a lamp out and hit " + user.mention() + " in the head and kills them.") 
                break
            if "cliff" in message.content.split():
                client.send_message(message.channel, message.author.mention() + " Binds and gags and throws " + user.mention() + " off a cliff to their death.")
                break
        else:
            if "lamp" in message.content.split():
                client.send_message(message.channel, message.author.mention() + " took a lamp out and hit them in the head and kills them.")
            if "cliff" in message.content.split():
                client.send_message(message.channel, message.author.mention() + " Binds and gags and throws them off a cliff to their death.")
    elif(message.content.startswith('--commands')):
         client.send_message(message.channel, botcommands)
    elif(message.content.startswith('--changelog')):
         client.send_message(message.channel, changelog)
    elif(message.content.startswith('--raid')):
        result = message.content[len("--raid "):].strip()
        print(result)
        client.send_message(message.channel, '@everyone RAID Boss ' + result)
    elif(message.content.startswith('--pyversion')):
        client.send_message(message.channel, message.author.mention() + " I was made with ``Python v2.7.10 (x86).``\n\nCompiled to exe by py2exe.")
#    elif (message.content.startswith('--playfile')):
#        cmd = 'node bot.js'
#        cmdargs = cmd.split()
#        p = subprocess.Popen(cmdargs)
    elif(message.content.startswith('--source')):
        client.send_message(message.channel, message.author.mention() + sourcelink)
    elif message.author.id == discord_user_id:
        if(message.content.startswith('--close')):
            client.send_message(message.channel, "**DecoraterBot Status: Offline**")
            os.startfile(".\Decorater.exe")
            client.logout()

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()
