#!/usr/bin/env python3
'''0. Writing strings to Redis
'''
import redis
import uuid
from typing import Union, Callable


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

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        '''Return data back to the desired format'''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Return data as utf-8 string'''
        return self._redis.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Return data as interger'''
        return self._redis.get(key, int)
