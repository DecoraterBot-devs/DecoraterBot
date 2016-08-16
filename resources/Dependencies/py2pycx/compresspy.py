# coding=utf-8
import api
import sys
import os
import getopt


def main(argv):
    if len(argv) < 1:
        sys.exit(2)
    try:
        options, arguments = getopt.getopt(argv, 'p:f:c:a:', ['path=', 'filename=', 'compression_level=', 'password='])
    except getopt.GetoptError:
        sys.exit(2)
    in_path = None
    filename = None
    czlevel = None
    pswd = None
    for option, argument in options:
        if option in ('p', '--path'):
            in_path = argument
        if option in ('f', '--filename'):
            filename = argument
        if option in ('c', '--compression-level'):
            czlevel = argument
        if option in ('a', '--password'):
            pswd = argument
    if pswd is not None:
        try:
            api.compress_protected_script(in_path, filename, cz_level=czlevel,password=pswd)
            print('Password Protected Script Compression Complete.')
        except api.NoPasswordSpecified as err:
            print('Error: {0}'.format(str(err)))
        except api.FileNotFound as err:
            print('Error: {0}'.format(str(err)))
        except api.FilePathNotProvided as err:
            print('Error: {0}'.format(str(err)))
        except api.FileNameNotProvided as err:
            print('Error: {0}'.format(str(err)))
    else:
        try:
            api.compress_script(in_path, filename, cz_level=czlevel)
            print('Script Compression Complete.')
        except api.FileNotFound as err:
            print('Error: {0}'.format(str(err)))
        except api.FilePathNotProvided as err:
            print('Error: {0}'.format(str(err)))
        except api.FileNameNotProvided as err:
            print('Error: {0}'.format(str(err)))

if __name__ == "__main__":
    main(sys.argv[1:])
