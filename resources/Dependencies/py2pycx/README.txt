This is a simple library that I really want to end up being shipped with python itself to allow loading of pycx files
through within normal import statements.
this is because if I do not than any pycx file that depends on another pycx file would not work right if it was decoded back to py.
So this means the files that handes the inport code needs to know about this format and to know how to decode it to the right ways.

Also included the pyc file for you to be able to see if you can look into it and add support for else: statements in if blocks.
(as it seems your decompile does not support else: (or knows how to decode it to insert them) statements)