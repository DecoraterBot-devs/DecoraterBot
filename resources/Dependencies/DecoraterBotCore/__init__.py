# coding=utf-8
"""
The MIT License (MIT)

Copyright (c) 2015-2016 AraHaan

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from . import Core
from . import BotConfigReader
from . import BotErrors
from . import Login
from . import BotCommands
from . import BotVoiceCommands
from . import BotLogs
from . import BotPMError
from . import Ignore
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


class DummyClass:
    """
        Class that is created solely for silencing PyCharm.
    """
    @staticmethod
    def __dummy2():
        Core.dummy()
        Login.dummy()
        BotCommands.dummy()
        BotConfigReader.dummy()
        BotVoiceCommands.dummy()
        BotLogs.dummy()
        BotPMError.dummy()
        BotErrors.dummy()
        Ignore.dummy()

del DummyClass
del Core.dummy
del Login.dummy
del BotCommands.dummy
del BotConfigReader.dummy
del BotVoiceCommands.dummy
del BotLogs.dummy
del BotPMError.dummy
del BotErrors.dummy
del Ignore.dummy


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
