# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import concurrent.futures

__all__ = ['BotException', 'MaxPlayersError',
           'CommandTimeoutError']


class BotException(Exception):
    """
    Base Class for Bot Errors.
    """
    pass


class MaxPlayersError(BotException):
    """
    Exception thrown when the user tries
    to add more players than the maximum
    number set.
    """
    pass


CommandTimeoutError = concurrent.futures.TimeoutError
