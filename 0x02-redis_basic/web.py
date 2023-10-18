#!/usr/bin/env python3
'''5. Implementing an expiring web cache and tracker
'''
import requests
import redis
from functools import wraps
from typing import Callable


cache = redis.Redis()


def cache_data(method: Callable) -> Callable:
    '''
    Count how many times methods called
    '''
    @wraps(method)
    def wrapper(*args, **kwargs) -> str:
        '''Increment the called method'''
        key_count = 'count:'.format(args[0])
        key_result = 'result:'.format(args[0])
        cache.incr(key_count)
        if cache.exists(key_result) == 1:
            return cache.get(key_result).decode('utf-8')
        # If not exists reset cache count & result
        respone = method(*args, **kwargs)
        cache.setex(key_result, 10, respone)
        return respone
    return wrapper


@cache_data
def get_page(url: str) -> str:
    '''Return HTML content of url'''
    return requests.get(url).text
