# coding=utf-8
"""
DecoraterBot
~~~~~~~~~~~~~~~~~~~

DecoraterBot

:copyright: (c) 2015-2022 AraHaan
:license: MIT, see LICENSE for more details.

"""
import sys
import gc
import asyncio

from DecoraterBotUtils.client import BotClient


async def main():
    """
    EntryPoint to DecoraterBot.
    """
    async with BotClient() as client:
        await client.start_bot()


if __name__ == '__main__':
    sys.dont_write_bytecode = True

    # in case there is leaks lets
    # tell the interpreter to clean
    # them up.
    gc.enable()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
