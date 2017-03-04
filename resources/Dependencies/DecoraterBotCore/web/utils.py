# coding=utf-8
"""..."""
import re


def parse_redis_url(redis_url):
    """..."""
    pattern = r'redis:\/\/([a-zA-Z0-9.]*):?([0-9]*)?'
    result = re.match(pattern, redis_url).groups()
    if result[1]:
        return (result[0],
                int(result[1]))
    else:
        return (result[0],
                6379)
