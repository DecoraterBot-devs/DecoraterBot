# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2018 AraHaan
:license: MIT, see LICENSE for more details.

"""
from DecoraterBotUtils.utils import BaseClient, config


__all__ = ['main', 'BotClient']


class BotClient(BaseClient):
    """
    Bot Main client Class.
    This is where the Events are Registered.
    """
    def __init__(self, **kwargs):
        super(BotClient, self).__init__(**kwargs)


def main():
    """
    EntryPoint to DecoraterBot.
    """
    BotClient(command_prefix=config.bot_prefix,
              description=config.description,
              pm_help=False)
