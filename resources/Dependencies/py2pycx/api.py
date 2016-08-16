# coding=utf-8
import os
import io
import zlib
import base64


class BaseErrors(Exception):
    '''
    Base Exceptions class.
    '''
    pass


class FilePathNotProvided(BaseErrors):
    '''
    Exception for When a Script File (Either Compressed or not) is not provided.
    '''
    pass


class FileNameNotProvided(BaseErrors):
    '''
    Exception for When a Script File is not provided is not provided.
    '''
    pass


class FileNotFound(BaseErrors):
    '''
    Exception for When a Script File (Either Compressed or not) is not found.
    '''
    pass


class NoPasswordSpecified(BaseErrors):
    '''
    Exception for When a Password is not specified for a Password Protected Script file.
    '''
    pass


class InvalidPassword(BaseErrors):
    '''
    Exception for when a Password is Incorrect.
    '''
    pass


class PasswordProtectedError(BaseErrors):
    '''
    Exception for when Trying to Decompress a Password Protected file in the Non-Password Protection 
    version of the Decompressor.
    '''
    pass


class NoPasswordPresent(BaseErrors):
    '''
    Exception for when the Password Protected Decompress Function is Called with a PYCX file that has 
    no password protection on it.
    '''
    pass


def compress_script(filepath, filename, cz_level=None):
    '''
    Compresses a Python Script.
    :param filepath: Path to the file to compress.
    :param filename: File name to compress.
    :param cz_level: Compression level (Max is 9) If None is provided then default is level 9.
    :return: None
    '''
    notfound = False
    if filepath is not None:
        if filename is not None:
            if cz_level is None:
                cz_level = 9
            filedata = None
            try:
                file = io.open(filepath + filename + '.py', "rb")
                if file is not None:
                    filedata = file.read()
                    file.close()
                base64data = base64.b64encode(filedata)
                czfiledata = b'PYCX' + zlib.compress(base64data, cz_level)
                czfileobj = open(filepath + filename + '.pycx', 'wb')
                if czfileobj is not None:
                    czfileobj.write(czfiledata)
                    czfileobj.close()
            except FileNotFoundError:
                notfound = True
            if notfound:
                raise FileNotFound('{0}.py was not found.'.format(filename))
        else:
            raise FileNameNotProvided('A File Name was not provided to compress a python script file.')
    else:
        raise FilePathNotProvided('A File Path was not provided to compress a python script file.')


def compress_protected_script(filepath, filename, cz_level=None, password=None):
    '''
    Same as decompress_script() but is for Decompressing password Protected pycx files.

    Password must be a byte string. This Function will then add the byte string in to the
    file (in a compressed form ofc).
    :param filepath: Path to the file to compress.
    :param filename: File name to compress.
    :param cz_level: Compression level (Max is 9) If None is provided then default is level 9.
    :return: None
    '''
    notfound = False
    if filepath is not None:
        if filename is not None:
            if password is not None:
                pswdata = b'&pw=' + base64.b64encode(password)
                if cz_level is None:
                    cz_level = 9
                filedata = None
                try:
                    file = io.open(filepath + filename + '.py', "rb")
                    if file is not None:
                        filedata = file.read()
                        file.close()
                    base64data = base64.b64encode(filedata)
                    czfiledata = b'PYCX' + pswdata + zlib.compress(base64data, cz_level)
                    czfileobj = open(filepath + filename + '.pycx', 'wb')
                    if czfileobj is not None:
                        czfileobj.write(czfiledata)
                        czfileobj.close()
                except FileNotFoundError:
                    notfound = True
                if notfound:
                    raise FileNotFound('{0}.py was not found.'.format(filename))
            else:
                raise NoPasswordSpecified('A Password was not specified to compress {0}.pycx'.format(filename))
        else:
            raise FileNameNotProvided('A File Name was not provided to compress a python script file.')
    else:
        raise FilePathNotProvided('A File Path was not provided to compress a python script file.')


def decompress_script(filepath, filename):
    '''
    Decompresses a Python Script.
    :param filepath: Path to the file to decompress.
    :param filename: File name to decompress.
    :return: None
    '''
    notfound = False
    if filepath is not None:
        if filename is not None:
            filedata = None
            try:
                file = io.open(filepath + filename + '.pycx', "rb")
                if file is not None:
                    filedata = file.read()
                    filedata = filedata[len(b'PYCX'):].strip()
                    file.close()
                if filedata.startswith(b'&pw='):
                    raise PasswordProtectedError('Cannot Cecompress {0}.pycx due to Password Protection on the file.'.format(filename))
                else:
                    decczfiledata = zlib.decompress(filedata)
                    base64decodeddata = base64.b64decode(decczfiledata)
                    decczfileobj = open(filepath + filename + '.py', 'wb')
                    if decczfileobj is not None:
                        decczfileobj.write(base64decodeddata)
                        decczfileobj.close()
            except FileNotFoundError:
                notfound = True
            if notfound:
                raise FileNotFound('{0}.pycx was not found.'.format(filename))
        else:
            raise FileNameNotProvided('A File Name was not provided to decompress a compressed python script file.')
    else:
        raise FilePathNotProvided('A File Path was not provided to decompress a compressed python script file.')


def decompress_protected_script(filepath, filename, password=None):
    '''
    Same as decompress_script() but is for Decompressing password Protected pycx files.

    Password must be a byte string. This Function will then check and see if the byte string
    is in the file (in a compressed form ofc).
    :param filepath: Path to the file to decompress.
    :param filename: File name to decompress.
    :param password: byte string.
    :return: None
    '''
    notfound = False
    if filepath is not None:
        if filename is not None:
            if password is not None:
                pswdata = base64.b64encode(password)
                filedata = None
                try:
                    file = io.open(filepath + filename + '.pycx', "rb")
                    if file is not None:
                        filedata = file.read()
                        filedata = filedata[len(b'PYCX'):].strip()
                        file.close()
                    if filedata.startswith(b'&pw='):
                        filedata = filedata[len(b'&pw='):].strip()
                        if filedata.startswith(pswdata):
                            filedata = filedata.strip(pswdata)
                            decczfiledata = zlib.decompress(filedata)
                            base64decodeddata = base64.b64decode(decczfiledata)
                            decczfileobj = open(filepath + filename + '.py', 'wb')
                            if decczfileobj is not None:
                                decczfileobj.write(base64decodeddata)
                                decczfileobj.close()
                        else:
                            raise InvalidPassword('The Password Provided is Incorrect.')
                    else:
                        raise NoPasswordPresent('The file {0}.pycx is not Password Protected.'.format(filename))
                except FileNotFoundError:
                    notfound = True
                if notfound:
                    raise FileNotFound('{0}.pycx was not found.'.format(filename))
            else:
                raise NoPasswordSpecified('A Password was not specified to decompress {0}.pycx'.format(filename))
        else:
            raise FileNameNotProvided('A File Name was not provided to decompress a compressed python script file.')
    else:
        raise FilePathNotProvided('A File Path was not provided to decompress a compressed python script file.')


def this_is_not_a_function_to_keep_this_coment_in_byte_codes():
    '''
    I would like for the data returned from this to be importable without  having to cache (only if 
    sys.dont_write_bytecode is True) and without having to generate the normal py file as well.
    Why do this? what is the point?
    The Point for this is to make a interface to make python scripts smaller.
    With a range of 1/3 ~ 1/2 (results vary from file to file) the original sizes this is a dam good api for that.
    the cool thing is it uses python modules that comes with it. No External libs. (yet)
    Sadly this means somehow either recoding the original import statement in probably the C code to python itself.
    or finding how it reads from the pyc files (hopefully from within a python script).
    __init__.py:
        Normal Size: 598 bytes
        Compressed Size: 492 bytes
    api.py (this file):
        Normal Size: 13603 bytes
        Compressed Size: 4163 bytes
    compresspy.py:
        Normal Size: 1810 bytes
        Compressed Size: 937 bytes
    decompresspy.py:
        Normal Size: 1946 bytes
        Compressed Size: 930 bytes
    '''
    pass


def dec_script(filepath, filename):
    '''
    A Version of decompress_script() that does not write a Decompressed file. Instead it returns the bytes of the
    decompressed data.

    This is useful for when you want to import a pycx file that does not have a decompressed copy of itself.

    This also makes it possible for the python interpreter to write bytecode for it as well if sys.dont_write_bytecode
    is not set to True.

    The pro about this is the file name is required minus the '.pycx' part.

    Another benefit of this is that it can reduce a py file's size down by 1/3 (sometimes more) because of the
    base64 -> zlib compreesed data.

    :param filepath: Path to the file to decompress.
    :param filename: File name to decompress.
    :return: File Bytes to decompressed file data. (no joke it returns bytes, not text, bytes!!!)
    '''
    if filepath is not None:
        if filename is not None:
            filedata = None
            file = io.open(filepath + filename + '.pycx', "rb")
            if file is not None:
                filedata = file.read()
                filedata = filedata.strip(b'PYCX')
                file.close()
            decczfiledata = zlib.decompress(filedata)
            base64decodeddata = base64.b64decode(decczfiledata)
            return base64decodeddata
        else:
            raise FileNameNotProvided('A File Name was not provided to decompress a compressed python script file.')
    else:
        raise FilePathNotProvided('A File Path was not provided to decompress a compressed python script file.')


def dec_protected_script(filepath, filename, password=None):
    '''
    A Version of dec_script() that Allows Decoding of Password Protected pycx files to byte data.
    :param filepath: Path to the file to decompress.
    :param filename: File name to decompress.
    :param password: Password (in bytes) to the file to decode to byte data.
    :return: File Bytes to decompressed file data. (no joke it returns bytes, not text, bytes!!!)
    '''
    if filepath is not None:
        if filename is not None:
            if password is not None:
                pswdata = base64.b64encode(password)
                filedata = None
                file = io.open(filepath + filename + '.pycx', "rb")
                if file is not None:
                    filedata = file.read()
                    filedata = filedata[len(b'PYCX'):].strip()
                    file.close()
                if filedata.startswith(b'&pw='):
                    filedata = filedata[len(b'&pw='):].strip()
                    if filedata.startswith(pswdata):
                        filedata = filedata[len(pswdata):].strip()
                        decczfiledata = zlib.decompress(filedata)
                        base64decodeddata = base64.b64decode(decczfiledata)
                        return base64decodeddata
                    else:
                        raise InvalidPassword('The Password Provided is Incorrect.')
                else:
                    raise NoPasswordPresent('The file {0}.pycx is not Password Protected.'.format(filename))
            else:
                raise NoPasswordSpecified('A Password was not specified to decompress {0}.pycx'.format(filename))
        else:
            raise FileNameNotProvided('A File Name was not provided to decompress a compressed python script file.')
    else:
        raise FilePathNotProvided('A File Path was not provided to decompress a compressed python script file.')
