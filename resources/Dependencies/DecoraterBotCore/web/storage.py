# coding=utf-8
"""..."""
import asyncio
import aioredis
from .utils import parse_redis_url


class Storage():
    """Adds a prefix to Redis"""
    def __init__(self, namespace, redis):
        self.namespace = namespace
        self.redis = redis

    async def set(self, key, value, expire=0):
        """..."""
        key = self.namespace + key
        return await self.redis.set(
            key,
            value,
            expire=expire
        )

    async def get(self, key):
        """..."""
        key = self.namespace + key
        return await self.redis.get(key)

    async def smembers(self, key):
        """..."""
        key = self.namespace + key
        return await self.redis.smembers(key)

    async def srem(self, key, value):
        """..."""
        key = self.namespace + key
        return await self.redis.srem(key, value)

    async def sadd(self, key, member, *members):
        """..."""
        key = self.namespace + key
        return await self.redis.sadd(key, member, *members)

    async def delete(self, key, *keys):
        """..."""
        key = self.namespace + key
        return await self.redis.delete(key, *keys)

    async def sort(self, key, *get_patterns, by=None, offset=None, count=None,
                   asc=None, alpha=False, store=None):
        """..."""
        key = self.namespace + key
        if by:
            by = self.namespace + by
        return await self.redis.sort(key, *get_patterns, by=by, offset=offset,
                                     count=None, asc=None, alpha=False,
                                     store=None)

    async def ttl(self, key):
        """..."""
        key = self.namespace + key
        return await self.redis.ttl(key)

    async def expire(self, key, timeout):
        """..."""
        key = self.namespace + key
        return await self.redis.expire(key, timeout)

    async def incr(self, key):
        """..."""
        key = self.namespace + key
        return await self.redis.incr(key)

    async def incrby(self, key, amount):
        """..."""
        key = self.namespace + key
        return await self.redis.incrby(key, amount)

    async def setnx(self, key, value):
        """..."""
        key = self.namespace + key
        return await self.redis.setnx(key, value)

    async def lpush(self, key, value, *values):
        """..."""
        key = self.namespace + key
        return await self.redis.lpush(key, value, *values)

    async def lrange(self, key, start, stop):
        """..."""
        key = self.namespace + key
        return await self.redis.lrange(key, start, stop)

    async def lrem(self, key, count, value):
        """..."""
        key = self.namespace + key
        return await self.redis.lrem(key, count, value)

    async def lset(self, key, index, value):
        """..."""
        key = self.namespace + key
        return await self.redis.lset(key, index, value)

    async def ltrim(self, start, stop):
        """..."""
        return await self.redis.ltrim(start, stop)
