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

from DecoraterBotUtils.readers import DbCredentialsReader, DbLocalizationReader
from DecoraterBotUtils.client import BotClient


async def main():
    """
    EntryPoint to DecoraterBot.
    """
    async with DbCredentialsReader() as cred_reader:
        async with DbLocalizationReader() as loc_reader:
            async with BotClient(
                    [cred_reader, loc_reader],
                    description=await loc_reader.get_str_async(5, await cred_reader.language),
                    activity_name=await loc_reader.get_str_async(3, await cred_reader.language),
                    activity_url=await loc_reader.get_str_async(6, await cred_reader.language)) as client:
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
