# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2018 AraHaan
:license: MIT, see LICENSE for more details.

"""
from DecoraterBotUtils.client import BotClient, config


__all__ = ['main']


async def main():
    """
    EntryPoint to DecoraterBot.
    """
    client = BotClient(
        description=config.description,
        pm_help=False)
    async with client:
        await client.login_helper()
