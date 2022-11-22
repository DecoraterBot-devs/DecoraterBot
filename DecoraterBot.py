# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import os
import sys
import gc
import asyncio

sys.dont_write_bytecode = True
try:
    import DecoraterBotCore
except ImportError:
    sys.path.append(
        os.path.join(
            sys.path[0],
            'resources',
            'Dependencies'))
    import DecoraterBotCore

# in case there is leaks lets
# tell the interpreter to clean
# them up.
gc.enable()

if __name__ == '__main__':
    try:
        asyncio.run(DecoraterBotCore.Core.main())
    except KeyboardInterrupt:
        pass
