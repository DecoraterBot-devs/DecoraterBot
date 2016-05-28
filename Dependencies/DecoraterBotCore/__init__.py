# coding=utf-8
import sys
from .Core import *
import logging
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
