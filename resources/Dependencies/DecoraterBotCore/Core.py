# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
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
    if config.shards > 0:
        BotClient(command_prefix=config.bot_prefix,
                  shard_id=config.run_on_shard,
                  shard_count=config.shards,
                  description=config.description,
                  pm_help=False)
    else:
        BotClient(command_prefix=config.bot_prefix,
                  description=config.description,
                  pm_help=False)
