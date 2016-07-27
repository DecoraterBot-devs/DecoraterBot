# -*- coding: utf-8 -*-

"""
DecoraterCore
~~~~~~~~~~~~~~~~~~~

Core to Decorater

:copyright: (c) 2015 Decorater
:license: MIT, see LICENSE for more details.

"""

from .Core import changewindowtitle, commands
from .OnLogin import on_login
from .Logininfo import login_info
import logging

__title__ = 'DecoraterCore'
__author__ = 'Decorater'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Decorater'
__version__ = '1.0.0.3'
__build__ = 0x1000003

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
