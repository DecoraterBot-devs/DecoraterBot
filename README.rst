DecoraterBot Async Version
==========================

|image0| |image1|

.. figure:: /resources/images/AppIcon/AS.png

What is DecoraterBot?
---------------------

DecoraterBot is a Discord bot that is written in
`Python <https://www.python.org/>`__. It is currently maintained and
developed by @\ `AraHaan <https://github.com/AraHaan>`__,
@\ `DavidNeon <https://github.com/DavidNeon>`__, and rarely
@\ `JakesDen <https://github.com/jakesden>`__.

Contributors
------------

@\ `AraHaan <https://github.com/AraHaan>`__ - Bot Developer

@\ `CheeseCast <https://github.com/CheeseCast>`__ - Documentation &
Spell-checker.. (hue)

@\ `DavidNeon <https://github.com/DavidNeon>`__ - Bot Developer, Code
Changer, & More.

@\ `JakesDen <https://github.com/jakesden>`__ - Assistant Bot Developer,
Code Changer, & More.

Commands
--------

View the list of bot commands `here </Commands.md>`__.

Future Updates
--------------

The bot gets updated and tested regularly. Pushes are released when
features are stable.

Rewrites
--------

This bot from time to time might go through some rewrites to fix major
and minor bugs in code.

Because of such it might sometimes means that it drops support for other
things.

A such major rewrite was the commands extension one and then soon after
a rewrite yet again to drop support for Python 3.4.

The reason for dropping support for 3.4 is because Discord.py will do
the same soon as well when 3.5 is released on Debian systems.

Configuration
-------------

To run this bot you will need 2 things:

    A working Discord Bot Token.

    Your Account ID

Configuration is in Credentials.json in ``\\resources\\ConfigData\\``.

More Documentation on setting that file **coming Soon™**.

After you have configurated the bot with a token you can run the bot
with 1 of the following ways:

Windows
=======

    with ``DecoraterBot-3.5.bat`` that uses the 32-bit version of the
    system installed Python 3.5 interpreter on windows.

    with ``DecoraterBot-3.6.bat`` that uses the 32-bit version of the
    system installed Python 3.6 interpreter on windows.

    with ``DecoraterBot64-3.5.bat`` that uses the 64-bit version of the
    system installed Python 3.5 interpreter on windows.

    with ``DecoraterBot64-3.6.bat`` that uses the 64-bit version of the
    system installed Python 3.6 interpreter on windows.

Note *Before running any of those above patch files you need to run one
of these two batch files to install dependencies on your version of
python you installed to*
``%SystemDrive\Python35``/``%SystemDrive%\Python35x64`` *for Python 3.5
or* ``%SystemDrive\Python36``/``%SystemDrive%\Python36x64`` *for Python
3.6*

    ``install_deps-3.5.bat`` installs dependencies on to the 32-bit
    version of the system installed Python 3.5 interpreter on windows.

    ``install_deps-3.6.bat`` installs dependencies on to the 32-bit
    version of the system installed Python 3.6 interpreter on windows.

    ``install_deps64-3.5.bat`` installs dependencies on to the 64-bit
    version of the system installed Python 3.5 interpreter on windows.

    ``install_deps64-3.6.bat`` installs dependencies on to the 64-bit
    version of the system installed Python 3.6 interpreter on windows.

Linux
=====

    with ``DecoraterBot-35.sh`` that uses the current installed Python
    3.5 Interpreter.

    with ``DecoraterBot-36.sh`` that uses the current installed Python
    3.6 Interpreter.

First things first you need to install to ensure you have ``libffi-dev``
installed. You will have to also install ``ffmpeg``.

Now you have to install all dependencies to the bot using these files
(only after you install ``libffi-dev`` and ``ffmpeg``):

    install\_deps-3.5.sh

    install\_deps-3.6.sh

However you will also need to ensure you have the latest ``libopus``
installed.

Other Platforms
===============

Not available yet.

Some of the other platforms however could easily be unofficially
supported. Some of those platforms could be mingw on Windows or if you
can get the bot to work on python 3.6.1 on cygwin that could work to.
Note: you would then need to compile ffmpeg from source.

I need command line things to execute python 3.5.0+ (3.6.1 recommended).
You have any other platforms you want the bot to support? Well send me
it's sys.platform value. The only thing stopping me is a few lines of
platform specific code.

Want to help with the bot?
--------------------------

Join the official Cheese.lab servers to help test and contribute to the
development of the bot.

|image2|

And the Bot's Original Server (Kinda dead right now):

|image3|

The Bots Partnered Server (Bot created by DavidNeon):

|image4|

*Documentation isn't finished yet.*

.. |image0| image:: https://api.codacy.com/project/badge/Grade/689e8253ad204350a57ef03cde0818fa
   :target: https://www.codacy.com/app/AraHaan/DecoraterBot?utm_source=github.com&utm_medium=referral&utm_content=AraHaan/DecoraterBot&utm_campaign=badger
.. |image1| image:: https://img.shields.io/github/issues/AraHaan/DecoraterBot.svg
   :target: https://github.com/AraHaan/DecoraterBot/issues
.. |image2| image:: https://discordapp.com/api/guilds/81812480254291968/widget.png?style=banner2
   :target: https://discord.gg/lab
.. |image3| image:: https://discordapp.com/api/guilds/121816417937915904/widget.png?style=banner2
   :target: https://discord.gg/hNMKZ5Z
.. |image4| image:: https.//discordapp.com/api/guilds/288018843304198144/widget.png?style=banner2
   :target: https://discord.gg/dxqFtjR
