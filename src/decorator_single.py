import datetime
import functools
import redis


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def single(max_processing_time: datetime.timedelta):
    """
    Декоратор, гарантирующий, что функция не будет выполняться параллельно
    на нескольких процессах/серверах.

    :param max_processing_time: Максимальное время удержания блокировки
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock_key = f"single_lock:{func.__module__}.{func.__name__}"
            lock_expire = int(max_processing_time.total_seconds())

            acquired = redis_client.set(lock_key, "1", nx=True, ex=lock_expire)

            if not acquired:
                return None
            try:
                return func(*args, **kwargs)
            finally:
                redis_client.delete(lock_key)

        return wrapper

    return decorator
