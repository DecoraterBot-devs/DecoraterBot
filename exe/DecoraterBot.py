# For this file.
import sys
import os
import traceback
import getopt
# Needed For DecoraterBot to function like this.
import asyncio
import json
import ctypes
import ctypes.util
import wsgiref
import wsgiref.handlers
import http.cookies
import html
import html.parser
import pathlib
import uuid
import cgi
import xml.etree
import xml.etree.ElementTree
import pipes
import fileinput


class runfile:
    def __init__(self, filename, filepath, debug, largeexcept):
        self.filename = filename
        self.filepath = filepath
        self.debug = debug  # Bool.
        self.largeexcept = largeexcept  # Bool.
        self.exename = sys.executable
        self.platform = None
        self.bits = ctypes.sizeof(ctypes.c_voidp)
        if self.bits == 4:
            self.platform = 'x86'
        elif self.bits == 8:
            self.platform = 'x64'
        self.filenamecheck = self.filename.replace('py', 'exe')
        if self.debug:
            print('DEBUG: {0}'.format(self.filenamecheck))
        self.exedir = None
        if self.exename.find(self.filenamecheck) != -1:
            self.exedir = self.exename.replace(self.filenamecheck, '')
        self.execheck = self.exename.replace(self.filename.replace('py', '') + '{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(self.platform, sys.platform, sys.implementation, sys.version_info), '')
        if self.debug:
            print('DEBUG: {0}'.format(self.execheck))
        self.execheck2 = None
        if self.exename.find(self.filenamecheck) != -1:
            self.execheck2 = self.exename.replace(self.filenamecheck, self.filename.replace('py', '') + '{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(self.platform, sys.platform, sys.implementation, sys.version_info))
            if self.debug:
                print('DEBUG: {0}'.format(self.execheck2))
        self.checkexe()
        self.isrunningintemp()  # To Check if sys.path[0] points to a temp folder (And if so reset it's value).
        self.runfile()  # To Execute the File.

    def runfile(self):
        compdir = self.filepath + self.filename
        if os.path.isfile(compdir):
            if self.debug:
                print('DEBUG: {0}'.format(compdir))
            c = compile(open(compdir).read(), self.filename, 'exec')
            exec(c)
        else:
            print('Fatal Error: \'{0}\' file not found.'.format(self.filename))
        #except FileNotFoundError:
        #    print('Fatal Error: \'{0}\' file not found.'.format(self.filename))
        #except Exception as e:
        #    if self.largeexcept:
        #        print(e)
        #    else:
        #        exceptiondata = traceback.format_exception_only(type(e), e)
        #        msg = exceptiondata[0].replace('\n', '')
        #        print(msg)

    def isrunningintemp(self):
        if self.filepath.find('\\AppData\\Local\\Temp') != -1:
            if self.debug:
                print('DEBUG: {0}'.format('Is this Called?'))
            if self.exename.find(self.filenamecheck) == -1:  #  to see if to look for the execuatable with a same file name.
                self.filepath = self.execheck
            else:
                print('This Cannot be used in other projects other than DecoraterBot unless you change the code to this.')
            if self.debug:
                print('DEBUG: {0}'.format(self.filepath))

    def checkexe(self):
        if self.exename.find(self.filenamecheck) != -1:
            print('The exe name is wrong. Renaming...')
            try:
                os.rename(self.execheck, self.execheck2)
            except FileExistsError:
                print('Fatal Error: File Exists. Cannot Rename.')
            sys.exit(1)

bits = ctypes.sizeof(ctypes.c_voidp)
def main(argv):
    if len(argv) < 1:
        if bits == 4:
            runfile('DecoraterBot.py', sys.path[0], False, True)
        if bits == 8:
            runfile('DecoraterBot.py', sys.path[0], False, True)
    try:
        options, arguments = getopt.getopt(argv, 'd:', ['debug='])
    except getopt.GetoptError:
        sys.exit(2)
    debug = None
    for option, argument in options:
        if option in ('d', '--debug'):
            debug = argument
    if debug is not None:
        if debug is True or debug is False:
            if bits == 4:
                runfile('DecoraterBot.py', sys.path[0], debug, True)
            if bits == 8:
                runfile('DecoraterBot.py', sys.path[0], debug, True)
        else:
            print('Value passed in --debug must be \'True\' or \'False\'.')

if __name__ == "__main__":
    main(sys.argv[1:])
