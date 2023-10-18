#!/usr/bin/env python3
'''0. Writing strings to Redis
'''
import redis
import uuid
from typing import Union


class Cache:
    '''Implementation of redis class that deals with REDIS'''

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Store data to Redis using the generated key'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
