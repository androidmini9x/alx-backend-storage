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
        key = 'count:'.format(url)
        if cache.exists(key) == 1:
            cache.incr(key)
        else:
            cache.setex(key, 10, 1)
        return method(url)
    return wrapper


@count_calls
def get_page(url: str) -> str:
    '''Return HTML content of url'''
    return requests.get(url).text
