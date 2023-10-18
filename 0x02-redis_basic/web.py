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
        key_result = 'cached:'.format(args[0])
        respone = cache.get(key_result)
        if respone:
            return respone.decode('utf-8')
        # If not exists reset cache count & result
        respone = method(*args, **kwargs)
        cache.incr(key_count)
        cache.set(key_result, respone)
        cache.expire(key_result, 10, respone)
        return respone
    return wrapper


@cache_data
def get_page(url: str) -> str:
    '''Return HTML content of particular url'''
    return requests.get(url).text
