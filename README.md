# DecoraterBot Portable Version



## What is DecoraterBot?

DecoraterBot is a Discord bot that is written in [Python](https://www.python.org/). It is currently maintained and developed by @[AraHaan](https://github.com/AraHaan)

## Future Updates

The bot gets updated and tested regularly. Pushes are released when features are stable.

## Configuration

To run this bot you will need 3 things:

> A working Discord Bot Token. 

> Your Account ID

> Your Bot's ID

Configuration is in Credentials.json in ``\\resources\\ConfigData\\``.

More Documentation on setting that file up **coming Soon™**.

After you have configurated the bot with a token you can run the bot with 1 of the following ways:

# Windows

> with ``DecoraterBot.bat`` that uses the 32-bit version of the Embedded Python 3.5 interpreter.

(Will use 3.6 when it is released as a replacement so stay tuned)( Voice Compatibility is #1).
> with ``DecoraterBot64.bat`` that uses the 64-bit version of the Embedded Python 3.5 interpreter.

(Will be replaced with 3.6 when released too.)
> with ``DecoraterBot.cpython-36.bat`` that uses the 32-bit version of the Embedded Python 3.6 interpreter. 

(Do not use unless you want Voice Commands to not work due to a ``nacl._sodium`` ImportError that cannot be fixed when the voice functions in Discord.py does ``import nacl.secret``. (This bat file will be deleted at the release of 3.6 to favor 3.6 throughout the entire bot. (Depends if nacl._sodium crap gets fixed.)

> with ``DecoraterBot64.cpython-36.bat`` that uses the 64-bit version of the Embedded Python 3.6 interpreter.

Again. Do not use this Alpha Interpreter unless you do not want Voice Channel Commands to work. (In Which Case you would be better of Setting the Credentials Setting to Disable the Voice Commands. I Will change the Message on the File that allows of this to another message Soon™. (This bat file will be deleted at the release of 3.6 to favor 3.6 throughout the entire bot. (Depends if nacl._sodium crap gets fixed.)

> with ``DecoraterBot.sln`` in Visual Studio 2015 Update 3.

Note: You Will have to use the Bat files above by right clicking them in the solution file.
Also I might be thinking about finally removing some of the folders with py files as I am thinking of makign most of them pyd's to have further optimizations to the bot's Error logs (eg function names to files that do not hold the specific errors). With that Said the lines that calls some functions then will not show.

# Fedora

Not available yet. I need python binaries for Python 3.5.2 and the other things for this.
You have any other platforms you want the bot to support? Well send me it's sys.platform value and the python binaries with ``cffi``, ``aiohttp`` and any other python package this comes with for that OS and I could add it to here. The only thing stopping me is the Binaries and a few lines of platform specific code.

## Contributors

@[AraHaan](https://github.com/AraHaan) - Bot Developer |
@[CheeseCast](https://github.com/CheeseCast) - Documentation & Spell-checker.. (hue)

## Commands

View the list of bot commands [here](https://github.com/Cheeselab/DecoraterBot/blob/Async-Portable/Commands.MD)

## Want to help with the bot? 

Join the official Cheese.lab servers to help test and contribute to the development of the bot.

[![](https://discordapp.com/api/servers/71324306319093760/widget.png?style=banner2)](https://discord.gg/cheese) 
[![](https://discordapp.com/api/servers/200406284288131072/widget.png?style=banner2)](https://discord.gg/m9GDqER)

And the Bot's Original Server (Kinda dead right now):

[![](https://discordapp.com/api/servers/121816417937915904/widget.png?style=banner2)](https://discord.gg/kSYStUq)

-

*Documentation isn't finished yet.*


