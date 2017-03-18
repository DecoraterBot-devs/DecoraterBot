# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
from . import Core
import logging


__title__ = 'DecoraterBotCore'
__author__ = 'Decorater'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015-2017 Decorater'
__version__ = '1.0.0.12'
__build__ = 0x100000c

__all__ = Core.__all__

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """
        Logger for DecoraterBot (Not really used but idrc).
        """

        def emit(self, record):
            """
            some random function that I dont care to use.
            :param record:
            :return:
            """
            pass

logging.getLogger(__name__).addHandler(NullHandler())
