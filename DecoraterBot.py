# coding=utf-8
"""
The MIT License (MIT)

Copyright (c) 2015-2016 AraHaan

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import os
import sys
sys.dont_write_bytecode = True
try:
    import discord
    import DecoraterBotCore
except ImportError:
    sepa = os.sep
    appendpath = "{0}{1}resources{1}Dependencies".format(sys.path[0], sepa)
    appendpath2 = None
    if not (sys.platform.startswith('linux')):
        appendpath2 = "{0}{1}dependencies.win32.zip".format(appendpath, sepa)
    else:
        appendpath2 = "{0}{1}dependencies.linux.zip".format(appendpath, sepa)
    sys.path.append(appendpath)
    sys.path.append(appendpath2)
    import discord
    import DecoraterBotCore


DecoraterBotCore.Core.BotClient().not_a_async_function()
