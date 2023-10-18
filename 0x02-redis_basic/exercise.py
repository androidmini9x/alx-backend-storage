#!/usr/bin/env python3
'''0. Writing strings to Redis
'''
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''
    Count how many times methods of the Cache class are called
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Increment the called method'''
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    Store the history of inputs and outputs for a particular function
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Save logs i/o to redis
        '''
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'
        output = method(self, *args, **kwargs)
        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, output)
        return output

    return wrapper


def replay(method: Callable) -> None:
    '''
    Display the history of calls of a particular function
    '''
    if method is None or \
            not hasattr(method, '__self__') or \
            not isinstance(method.__self__, Cache):
        return
    store = method.__self__
    count_calls = 0
    if store.get(method.__qualname__) is not None:
        count_calls = int(store.get(method.__qualname__))
    print('{} was called {} times:'.format(method.__qualname__, count_calls))
    inputs = store._redis.lrange("{}:inputs".format(method.__qualname__),
                                 0, -1)
    outputs = store._redis.lrange("{}:outputs".format(method.__qualname__),
                                  0, -1)
    for ins, out in zip(inputs, outputs):
        print('{}(*{}) -> {}'.format(method.__qualname__,
                                     ins.decode('utf-8'),
                                     out.decode('utf-8')))


class Cache:
    '''Implementation of redis class that deals with REDIS'''

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
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
