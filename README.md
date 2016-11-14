# DecoraterBot Portable Version

[![Coverage Status](https://coveralls.io/repos/github/AraHaan/DecoraterBot/badge.svg)](https://coveralls.io/github/AraHaan/DecoraterBot)
[![issues](https://img.shields.io/github/issues/{AraHaan}/DecoraterBot.svg)](https://github.com/{AraHaan}/DecoraterBot/issues)


## What is DecoraterBot?

DecoraterBot is a Discord bot that is written in [Python](https://www.python.org/). It is currently maintained and developed by @[AraHaan](https://github.com/AraHaan)

## Future Updates

The bot gets updated and tested regularly. Pushes are released when features are stable.

## Configuration

To run this bot you will need 2 things:

> A working Discord Bot Token. 

> Your Account ID

Configuration is in Credentials.json in ``\\resources\\ConfigData\\``.

More Documentation on setting that file **coming Soon™**.

After you have configurated the bot with a token you can run the bot with 1 of the following ways:

# Windows

> with ``DecoraterBot.bat`` that uses the 32-bit version of the Embedded Python 3.5 interpreter.

(Will use 3.6 when it is released as a replacement so stay tuned)(Voice Compatibility is #1).
> with ``DecoraterBot64.bat`` that uses the 64-bit version of the Embedded Python 3.5 interpreter.

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

I need command line things to execute python 3.4.2+ (3.5.2 recommended).
You have any other platforms you want the bot to support?
Well send me it's sys.platform value. The only thing stopping me is a few lines of platform specific code.

## Contributors

@[AraHaan](https://github.com/AraHaan) - Bot Developer |
@[CheeseCast](https://github.com/CheeseCast) - Documentation & Spell-checker.. (hue)

## Commands

View the list of bot commands [here](https://github.com/Cheeselab/DecoraterBot/blob/Async-Portable/Commands.MD)

## Want to help with the bot? 

Join the official Cheese.lab servers to help test and contribute to the development of the bot.

[![](https://discordapp.com/api/guilds/71324306319093760/widget.png?style=banner2)](https://discord.gg/lab)

And the Bot's Original Server (Kinda dead right now):

[![](https://discordapp.com/api/guilds/121816417937915904/widget.png?style=banner2)](https://discord.gg/kSYStUq)

-

*Documentation isn't finished yet.*


