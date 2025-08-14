import random
import time
import redis


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    LUA_SCRIPT = """
    local key     = KEYS[1]
    local now     = tonumber(ARGV[1])
    local period  = tonumber(ARGV[2])
    local limit   = tonumber(ARGV[3])

    -- Удаляем записи старше окна
    redis.call('ZREMRANGEBYSCORE', key, 0, now - period)

    -- Считаем количество оставшихся запросов
    local count = redis.call('ZCARD', key)

    if count < limit then
        -- Добавляем текущий запрос
        redis.call('ZADD', key, now, tostring(now))
        return 1
    else
        return 0
    end
    """

    def __init__(
        self,
        name="rate_limiter",
        limit=5,
        period=3,
        host="localhost",
        port=6379,
        db=0,
    ):
        self.name = name
        self.limit = limit
        self.period = period
        self.redis = redis.StrictRedis(
            host=host, port=port, db=db, decode_responses=True
        )
        self._lua = self.redis.register_script(self.LUA_SCRIPT)

    def test(self) -> bool:
        now = time.time()
        result = self._lua(
            keys=[self.name], args=[now, self.period, self.limit]
        )
        return bool(result)


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # Какая-то бизнес логика
        pass


if __name__ == '__main__':
    rate_limiter = RateLimiter()

    for _ in range(50):
        time.sleep(random.randint(1, 2))
        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
