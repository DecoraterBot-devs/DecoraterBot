# coding=utf-8
from .api import *
import logging

"""
py2pycx
~~~~~~~~~~~~~~~~~~~

API for Compressing Python Scripts

:copyright: (c) 2016 Decorater
:license: MIT, see LICENSE for more details.

"""

__title__ = 'DecoraterBotCore'
__author__ = 'Decorater'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Decorater'
__version__ = '0.1.0'
__build__ = 0x00100

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
