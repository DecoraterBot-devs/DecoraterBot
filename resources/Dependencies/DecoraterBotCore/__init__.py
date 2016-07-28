# coding=utf-8
import sys
from .Core import *
import logging
"""
    DecoraterBot's source is protected by Cheese.lab industries Inc. Even though it is Open Source
    any and all users waive the right to say that this bot's code was stolen when it really was not.
    Me @Decorater the only core developer of this bot do not take kindly to those false Allegations.
    it would piss any DEVELOPER OFF WHEN THEY SPEND ABOUT A YEAR CODING STUFF FROM SCRATCH AND THEN BE ACCUSED OF SHIT LIKE THIS.
    
    So, do not do it. If you do Cheese.lab Industries Inc. Can and Will do after you for such cliams that it deems untrue.
    
    Cheese.lab industries Inc. Belieces in the rights of Original Developers of bots. They do not take kindly to BULLSHIT.
    
    Any and all Developers work all the time, many of them do not get paid for their hard work.
    
    I am one of those who did not get paid even though I am the original Developer I coded this bot from the bottom with no lines of code at all.
    
    And how much money did I get from it for my 11 months or so of working on it? None- yeah thats right 0$ how pissed can someone be?
    Exactly I have over stretched my relatives money that they paid for Internet and power for my computer so that way I can code my bot.
    
    However shit does go out of the Fan with a possible 600$ or more that my Laptop Drastically needs to Repairs as it is 10 years old and is falling apart
    
    I am half tempted myself to pulling this bot from github and making it on patrion that boobot is also on to help me with my development needs.
    
    So, as such I accept issue requests, but please do not give me bullshit I hate it as it makes everything worse than the way it is.
    
    You do have the right however to:
        -> Contribute to the bot's development.
        -> fix bugs.
        -> add commands.
        -> help finish the per server config (has issues)
        -> update the Voice commands to be better (and not use globals which is 1 big thing that kills it).

    But keep in mind any and all Changes you make can and will be property of Cheese.lab Induestries Inc.
"""
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2016 Decorater
:license: MIT, see LICENSE for more details.

"""

__title__ = 'DecoraterBotCore'
__author__ = 'Decorater'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Decorater'
__version__ = '1.0.0.12'
__build__ = 0x100000c

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
