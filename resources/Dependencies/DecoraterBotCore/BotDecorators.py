# coding=utf-8
import asyncio
from functools import wraps


def async_classmethod(func):
    """
        Decorator made to help out on making a function passed
        a classmethod and a coroutine.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return classmethod(asyncio.coroutine(wrapper))

def async_staticmethod(func):
    """
        Decorator made to help out on making a function passed
        a staticmethod and a coroutine.

        Note: Not used in DecoraterBot.
    """
    @wraps(func)
    def wrapper2(*args, **kwargs):
        return func(*args, **kwargs)
    return staticmethod(asyncio.coroutine(wrapper2))
