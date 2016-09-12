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
import ctypes
try:
    import discord
except ImportError:
    sepa = os.sep
    bits = ctypes.sizeof(ctypes.c_voidp)
    if bits == 4:
        platform = 'x86'
    elif bits == 8:
        platform = 'x64'
    path = sys.path[0]
    if path.find('\\AppData\\Local\\Temp') != -1:
        path = sys.executable.strip('DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(platform, sys.platform, sys.implementation, sys.version_info))
    appendpath = "{0}{1}resources{1}Dependencies".format(path, sepa)
    appendpath2 = "{0}{1}dependencies.{2}.{3.name}-{4.major}{4.minor}{4.micro}.zip".format(appendpath, sepa,
                                                                                           sys.platform,
                                                                                           sys.implementation,
                                                                                           sys.version_info)
    sys.path.append(appendpath2)
    if sys.platform.startswith("win"):
        appendpath3 = "{0}{1}resources{1}Dependencies{1}win32-deps".format(path, sepa)
        sys.path.append(appendpath3)
    import discord
try:
    import DecoraterBotCore
except ImportError:
    sepa = os.sep
    bits = ctypes.sizeof(ctypes.c_voidp)
    if bits == 4:
        platform = 'x86'
    elif bits == 8:
        platform = 'x64'
    path = sys.path[0]
    if path.find('\\AppData\\Local\\Temp') != -1:
        path = sys.executable.strip('DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(platform, sys.platform, sys.implementation, sys.version_info))
    appendpath = "{0}{1}resources{1}Dependencies".format(path, sepa)
    sys.path.append(appendpath)
    import DecoraterBotCore


DecoraterBotCore.Core.BotClient().not_a_async_function()
