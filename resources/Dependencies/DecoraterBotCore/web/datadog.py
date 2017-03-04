# coding=utf-8
"""..."""
import logging
from functools import wraps

import aiomeasures

log = logging.getLogger('discord')


def existance_check(f):
    """..."""
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """..."""
        if self.agent:
            func = getattr(self.agent, f.__name__)
            return func(*args, **kwargs)
        else:
            log.debug('No Datadog agent found...')
    return wrapper


class DDAgent:
    """..."""
    def __init__(self, dd_agent_url=None):
        self.dd_agent_url = dd_agent_url
        self.agent = None

        if dd_agent_url:
            self.agent = aiomeasures.Datadog(dd_agent_url)

    @existance_check
    def send(self, *args, **kwargs):
        """..."""
        pass

    @existance_check
    def set(self, *args, **kwargs):
        """..."""
        pass

    @existance_check
    def event(self, *args, **kwargs):
        """..."""
        pass

    @existance_check
    def incr(self, *args, **kwargs):
        """..."""
        pass
