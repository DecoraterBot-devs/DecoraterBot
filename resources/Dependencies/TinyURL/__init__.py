# -*- coding: utf-8 -*-

"""
TinyURL
~~~~~~~~~~~~~~~~~~~

TinyURL for Python 3.x

:copyright: (c) 2016 Decorater
:license: MIT, see LICENSE for more details.

"""
from .TinyURL import create_one, create
import logging

__title__ = 'TinyURL'
__author__ = 'Decorater'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Decorater'
__version__ = '0.1.1'
__build__ = 0x000101

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
