#!/usr/bin/env python3
'''5. Implementing an expiring web cache and tracker
'''
import requests
import redis
from functools import wraps
from typing import Callable


cache = redis.Redis()


def count_calls(method: Callable) -> Callable:
    '''
    Count how many times methods called
    '''
    @wraps(method)
    def wrapper(url) -> str:
        '''Increment the called method'''
        key_count = 'count:'.format(url)
        key_result = 'result:'.format(url)
        cache.incr(key_count)
        if cache.exists(key_result) == 1:
            return cache.get(key_result).decode('utf-8')
        # If not exists reset cache count & result
        respone = method(url)
        cache.set(key_count, 0)
        cache.setex(key_result, 10, respone)
        return respone
    return wrapper


@count_calls
def get_page(url: str) -> str:
    '''Return HTML content of url'''
    return requests.get(url).text
