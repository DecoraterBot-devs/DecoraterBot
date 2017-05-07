DecoraterBot Async Version
==========================

|image0| |image1|

.. figure:: /resources/images/AppIcon/AS.png

What is DecoraterBot?
---------------------

DecoraterBot is an extendable Discord bot that is written in
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

View the list of bot commands
`here <https://github.com/DecoraterBot-devs/DecoraterBot-cogs/blob/master/Commands.md>`__.

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

Submitting Plugins
------------------

As of April 8th 2017 it is now not recommended to submit plugins to this
repository. Submit them to
`here <https://github.com/DecoraterBot-devs/DecoraterBot-cogs>`__ as a
pull request instead.

Used Events
-----------

View the list of used events `here </UsedEvents.md>`__.

Configuration
-------------

To run this bot you will need 2 things:

    A working Discord Bot Token.

    Your Account ID

Configuration is in ``\\resources\\ConfigData\\``.

Before setting configuration be sure to copy
``Credentials_example.json`` to ``Credentials.json``.

More Documentation on setting that file is `here </Credentials.md>`__.

After you have configurated the bot with a token you can run the bot
like so:

Windows
=======

    with ``DecoraterBot.bat`` that uses the version of python you have
    on the windows path environment variable.

Note: *Before running any of those above patch files you need to run
this file below to install dependencies on your version of python you
installed.*

    ``install_deps.bat`` installs dependencies on the version of python
    you have on the windows path environment variable.

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

*Documentation isn't finished yet.*

.. |image0| image:: https://api.codacy.com/project/badge/Grade/689e8253ad204350a57ef03cde0818fa
   :target: https://www.codacy.com/app/AraHaan/DecoraterBot?utm_source=github.com&utm_medium=referral&utm_content=AraHaan/DecoraterBot&utm_campaign=badger
.. |image1| image:: https://img.shields.io/github/issues/DecoraterBot-devs/DecoraterBot.svg
   :target: https://github.com/DecoraterBot-devs/DecoraterBot/issues
.. |image2| image:: https://discordapp.com/api/guilds/81812480254291968/widget.png?style=banner2
   :target: https://discord.gg/lab
.. |image3| image:: https://discordapp.com/api/guilds/121816417937915904/widget.png?style=banner2
   :target: https://discord.gg/hNMKZ5Z
