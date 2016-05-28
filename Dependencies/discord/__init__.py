# -*- coding: utf-8 -*-

"""
Discord API Wrapper
~~~~~~~~~~~~~~~~~~~

A basic wrapper for the Discord API.

:copyright: (c) 2015-2016 Rapptz
:license: MIT, see LICENSE for more details.

"""

__title__ = 'discord'
__author__ = 'Rapptz'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015-2016 Rapptz'
__version__ = '0.10.0-alpha'

# noinspection PyPep8
from .client import Client
# noinspection PyPep8
from .user import User
# noinspection PyPep8
from .game import Game
# noinspection PyPep8
from .channel import Channel, PrivateChannel
# noinspection PyPep8
from .server import Server
# noinspection PyPep8
from .member import Member
# noinspection PyPep8
from .message import Message
# noinspection PyPep8
from .errors import *
# noinspection PyPep8
from .permissions import Permissions
# noinspection PyPep8
from .role import Role
# noinspection PyPep8
from .colour import Color, Colour
# noinspection PyPep8
from .invite import Invite
# noinspection PyPep8
from .object import Object
# noinspection PyPep8
from . import utils, opus, compat
# noinspection PyPep8
from .voice_client import VoiceClient
# noinspection PyPep8
from .enums import ChannelType, ServerRegion, Status
# noinspection PyPep8
from collections import namedtuple
# noinspection PyPep8
import logging

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=10, micro=0, releaselevel='alpha', serial=0)

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
