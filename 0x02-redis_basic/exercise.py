#!/usr/bin/env python3
'''
0. Writing strings to Redis
'''
import redis
import uuid
from typing import Union


class Cache:
    '''Implementation of redis class'''
    def __init__(self) -> None:
        '''Init redis cache'''
        self._redis = redis.Redis()
        self._redis.flushall(True)

    def store(self, data: Union[str, int, bytes, float]) -> str:
        '''Store data by generated key'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
