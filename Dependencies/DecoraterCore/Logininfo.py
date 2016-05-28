# coding=utf-8
import os
import discord
import os.path
import asyncio
import sys
import json
import io
PATH = str(sys.path[0]) + '\\ConfigData\\selfbot.json'


def login_info(client):
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        credsfile = io.open(PATH, 'r')
        credentials = json.load(credsfile)
        discord_user_email = str(credentials['email'][0])
        if discord_user_email == 'None':
            discord_user_email = None
        discord_user_password = str(credentials['password'][0])
        if discord_user_password == 'None':
            discord_user_password = None
        discord_user_token = str(credentials['token'][0])
        if discord_user_token == 'None':
            discord_user_token = None
        try:
            client.run(discord_user_email, discord_user_password, discord_user_token)
        except discord.errors.GatewayNotFound:
            print('The Gateway was not found. API Downtime?')
            return
        except discord.errors.LoginFailure:
            print('Cannot login for some reason. Maybe incorrect email or password.')
            return
        except TypeError:
            return
        except KeyboardInterrupt:
            return
        except discord.errors.InvalidToken:
            print("Invalid Token was specified for the bot.")
            sys.exit(2)
    else:
        print("selfbot.json does not exist. It must be present in order for this bot to work.")
        sys.exit(2)
