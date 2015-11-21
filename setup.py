from distutils.core import setup
import py2exe

includes = ['cffi', 'idna', 'pycparser', 'setuptools', 'ipaddress', 'six']
excludes = []
packages = []
dll_excludes = []

setup(
    options = {"py2exe": {"includes": includes, 
                          "bundle_files": 1, 
                         }
              },
    zipfile = None,
    console=['DecoraterBot.py']
)

setup(
    options = {"py2exe": {"includes": includes, 
                          "bundle_files": 1, 
                         }
              },
    zipfile = None,
    console=['Decorater.py']
)