# DecoraterBot Portable Version

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/689e8253ad204350a57ef03cde0818fa)](https://www.codacy.com/app/AraHaan/DecoraterBot?utm_source=github.com&utm_medium=referral&utm_content=AraHaan/DecoraterBot&utm_campaign=badger)
[![issues](https://img.shields.io/github/issues/AraHaan/DecoraterBot.svg)](https://github.com/AraHaan/DecoraterBot/issues)


## What is DecoraterBot?

DecoraterBot is a Discord bot that is written in [Python](https://www.python.org/). It is currently maintained and developed by @[AraHaan](https://github.com/AraHaan)

## Future Updates

The bot gets updated and tested regularly. Pushes are released when features are stable.

## Rewrites

This bot from time to time might go through some rewrites to fix major and minor bugs in code.

Because of such it might sometimes means that it drops support for other things.

A such major rewrite was the commands extension one and then soon after a rewrite yet again to drop support for Python 3.4.

The reason for dropping support for 3.4 is because Discord.py will do the same soon as well when 3.5 is released on Debian systems.

## Configuration

To run this bot you will need 2 things:

> A working Discord Bot Token. 

> Your Account ID

Configuration is in Credentials.json in ``\\resources\\ConfigData\\``.

More Documentation on setting that file **coming Soon™**.

After you have configurated the bot with a token you can run the bot with 1 of the following ways:

# Windows

> with ``DecoraterBot.bat`` that uses the 32-bit version of the system installed Python 3.5+ interpreter on windows.

> with ``DecoraterBot64.bat`` that uses the 64-bit version of the system installed Python 3.5+ interpreter on windows.

(Will be replaced with 3.6 when released too.)

> with ``DecoraterBot.sln`` in Visual Studio 2015 Update 3.

Note: You Will have to use the Bat files above by right clicking them in the solution file.
Also I might be thinking about finally removing some of the folders with py files as I am thinking of makign most of them pyd's to have further optimizations to the bot's Error logs (eg function names to files that do not hold the specific errors). With that Said the lines that calls some functions then will not show.

# Linux

> with ``DecoraterBot.sh`` that uses the current installed Python Interpreter (Python 3.5.2 recommended).

You will also have to install the following as well in order to run the bot:

> aiohttp (latest perfered)

> pynacl

> cffi (should be installed when pynacl is installed usually)


Luckily the following file should be able to handle the installation:

> install_deps.linux.sh

# Other Platforms

Not available yet.

Some of the other platforms however could easily be unofficially supported. Some of those platforms could be mingw on Windows or if you can get the bot to work on python 3.6.1 on cygwin that could work to. Note: you would then need to compile ffmpeg from source.

I need command line things to execute python 3.5.0+ (3.5.2 recommended).
You have any other platforms you want the bot to support?
Well send me it's sys.platform value. The only thing stopping me is a few lines of platform specific code.

## Contributors

@[AraHaan](https://github.com/AraHaan) - Bot Developer |
@[CheeseCast](https://github.com/CheeseCast) - Documentation & Spell-checker.. (hue)
@[DavidNeon](https://github.com/DavidNeon) - Bot Developer | Code Changer & More.

## Commands

View the list of bot commands [here](https://github.com/AraHaan/DecoraterBot/blob/Async-Portable/Commands.MD)

## Want to help with the bot? 

Join the official Cheese.lab servers to help test and contribute to the development of the bot.

[![](https://discordapp.com/api/guilds/81812480254291968/widget.png?style=banner2)](https://discord.gg/lab)

And the Bot's Original Server (Kinda dead right now):

[![](https://discordapp.com/api/guilds/121816417937915904/widget.png?style=banner2)](https://discord.gg/kSYStUq)

The Bots Partnered Server (Bot created by DavidNeon)
[![](https.//discordapp.com/api/guilds/288018843304198144/widget.png?style=banner2)](https://discord.gg/dxqFtjR)

*Documentation isn't finished yet.*


