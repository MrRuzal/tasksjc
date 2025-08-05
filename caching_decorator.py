'''
Реализуйте lru_cache декоратор.

Требования:

Декоратор должен кешировать результаты вызовов функции на основе её аргументов.
Если функция вызывается с теми же аргументами, что и ранее, возвращайте результат
из кеша вместо повторного выполнения функции.
Декоратор должно быть возможно использовать двумя способами:
с указанием максимального кол-ва элементов и без.
'''

from functools import wraps
from collections import OrderedDict
import unittest.mock


def lru_cache(*args, **kwargs):
    if len(args) == 1 and callable(args[0]) and not kwargs:
        return lru_cache(maxsize=128)(args[0])

    maxsize = kwargs.get('maxsize', None)

    def decorator(func):
        cache = OrderedDict()
        hits = misses = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal hits, misses
            key = (args, tuple(sorted(kwargs.items())))

            if key in cache:
                hits += 1
                cache.move_to_end(key)
                return cache[key]

            misses += 1
            result = func(*args, **kwargs)
            cache[key] = result

            if maxsize is not None and len(cache) > maxsize:
                cache.popitem(last=False)
            return result

        wrapper.cache_info = lambda: {
            'hits': hits,
            'misses': misses,
            'maxsize': maxsize,
            'currsize': len(cache),
        }
        wrapper.cache_clear = cache.clear
        return wrapper

    return decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == '__main__':

    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
