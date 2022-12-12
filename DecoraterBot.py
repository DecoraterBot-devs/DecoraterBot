# coding=utf-8
"""
DecoraterBot
~~~~~~~~~~~~~~~~~~~

DecoraterBot

:copyright: (c) 2015-2022 AraHaan
:license: MIT, see LICENSE for more details.

"""
import os
import sys
import gc
import asyncio

from DecoraterBotUtils.client import BotClient, config


async def main():
    """
    EntryPoint to DecoraterBot.
    """
    client = BotClient(
        description=config.description,
        pm_help=False)
    async with client:
        await client.login_helper()


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    sys.path.append(os.path.join(sys.path[0], 'resources', 'Dependencies'))

    # in case there is leaks lets
    # tell the interpreter to clean
    # them up.
    gc.enable()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
