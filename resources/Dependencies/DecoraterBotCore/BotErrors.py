# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import concurrent.futures

__all__ = ['MaxPlayersError', 'CogUnloadError',
           'CommandTimeoutError']


class MaxPlayersError(Exception):
    """
    Exception thrown when the user tries
    to add more players than the maximum
    number set.
    """
    pass


class CogUnloadError(Exception):
    """
    raised when an error occurs when
    unloading a cog.
    """
    pass


CommandTimeoutError = concurrent.futures.TimeoutError
