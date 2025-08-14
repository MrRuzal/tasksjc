import json
import redis


class RedisQueue:
    def __init__(self, name="queue", host="localhost", port=6379, db=0):
        self.name = name
        self.redis = redis.StrictRedis(
            host=host, port=port, db=db, decode_responses=True
        )

    def publish(self, msg: dict):
        """
        Добавляет сообщение в очередь.

        :param msg: Сообщение в виде словаря
        """
        if not isinstance(msg, dict):
            raise ValueError("Message must be a dictionary")
        self.redis.lpush(self.name, json.dumps(msg))

    def consume(self) -> dict:
        """
        Извлекает сообщение из очереди в порядке FIFO.
        Возвращает dict или None, если очередь пуста.
        """
        data = self.redis.rpop(self.name)
        if data is None:
            return None
        return json.loads(data)


if __name__ == '__main__':
    q = RedisQueue()
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
