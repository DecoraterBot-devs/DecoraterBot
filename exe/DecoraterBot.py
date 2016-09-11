import sys
import os
import traceback
# Needed For DecoraterBot to function like this.
import asyncio
import json
import ctypes
import ctypes.util
import wsgiref
import wsgiref.handlers
import http.cookies
import pathlib
import uuid
import cgi
import xml.etree
import xml.etree.ElementTree
import HTMLParser

class runfile:
    def __init__(self, filename, filepath, debug):
        self.filename = filename
        self.filepath = filepath
        self.debug = debug  # Bool.
        self.isrunningintemp()  # To Check if sys.path[0] points to a temp folder (And if so reset it's value).
        self.runfile()  # To Execute the File.

    def runfile(self):
        try:
            c = compile(open(self.filepath + os.sep + self.filename).read(), self.filename, 'exec')
            exec(c)
        except FileNotFoundError:
            print('Fatal Error: \'{0}\' file not found.'.format(self.filename))
        except Exception as e:
            exceptiondata = traceback.format_exception_only(type(e), e)
            msg = exceptiondata[0].replace('\n', '')
            print(msg)

    def isrunningintemp(self):
        if self.filepath.find('\\AppData\\Local\\Temp') != -1:
            if self.debug:
                print('Is this Called?')
            if sys.executable.find(self.filename.replace('.py', '')) != -1:  #  to see if to look for the execuatable with a same file name.
                self.filepath = sys.executable.strip(self.filename.replace('py', 'exe'))
            else:
                print('This Cannot be used in other projects other than DecoraterBot unless you change the code to this.')
            if self.debug:
                print(self.filepath)

# runfile('test.py', sys.path[0], False)
# runfile('bad.py', sys.path[0], True)
runfile('DecoraterBot.py', sys.path[0], False)
