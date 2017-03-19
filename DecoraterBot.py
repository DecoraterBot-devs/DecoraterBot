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
sys.dont_write_bytecode = True
try:
    import DecoraterBotCore
except ImportError:
    sepa = os.sep
    path = sys.path[0]
    appendpath = "{0}{1}resources{1}Dependencies".format(path, sepa)
    sys.path.append(appendpath)
    import DecoraterBotCore
gc.enable()


# Note: All new commands should be added via plugins.
# Also some normal commands can move to plugins as well at any moment in time.

# However this excludes fixing bugs or anything else in normal commands within the commands folder.

if __name__ == '__main__':
    DecoraterBotCore.Core.main()
