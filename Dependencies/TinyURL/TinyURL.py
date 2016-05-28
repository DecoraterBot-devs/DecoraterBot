# coding=utf-8
import sys
import urllib
import optparse

API_CREATE = "http://tinyurl.com/api-create.php"
DEFAULT_DELIM = "\n"
USAGE = """%prog [options] url [url url ...]
 
 + __doc__ + 
Any number of urls may be passed and will be returned
in order with the given delimiter, default=%r
 % DEFAULT_DELIM
"""
ALL_OPTIONS = (
    (('-d', '--delimiter'), 
        dict(dest='delimiter', default=DEFAULT_DELIM, 
             help='delimiter for returned results')),
)


def _build_option_parser():
    prs = optparse.OptionParser(usage=USAGE)
    for args, kwargs in ALL_OPTIONS:
        prs.add_option(*args, **kwargs)
    return prs


def create_one(url):
    url_data = urllib.parse.urlencode(dict(url=url))
    byte_data = str.encode(url_data)
    ret = urllib.request.urlopen(API_CREATE, data=byte_data).read().strip()
    almost_result = str(ret)
    closer_result = almost_result.strip("b")
    result = closer_result.strip("'")
    return result


def create(*urls):
    for url in urls:
        yield create_one(url)


def main(sysargs=sys.argv[:]):
    parser = _build_option_parser()
    opts, urls = parser.parse_args(sysargs[1:])
    for url in create(*urls):
        sys.stdout.write(url + opts.delimiter)
    return 0


if __name__ == '__main__':
    sys.exit(main())
