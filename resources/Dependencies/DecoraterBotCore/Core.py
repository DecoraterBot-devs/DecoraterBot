# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2018 AraHaan
:license: MIT, see LICENSE for more details.

"""
from DecoraterBotUtils.utils import BotClient, config


__all__ = ['main']


def main():
    """
    EntryPoint to DecoraterBot.
    """
    BotClient(command_prefix=config.bot_prefix,
              description=config.description,
              pm_help=False)
