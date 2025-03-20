import redis


class RedisManager:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """
        Менеджер для работы с Redis.

        :param redis_url: URL подключения к Redis. По умолчанию локальный сервер.
        """
        self.conn = redis.Redis.from_url(url=redis_url)

    def lock_set(self, name: str, expire: int = 3600) -> bool:
        """
        Устанавливает блокировку по указанному имени.

        :param name: Имя блокировки.
        :param expire: Время жизни блокировки в секундах (по умолчанию 1 час).
        :return: True, если блокировка успешно установлена, иначе False.
        """
        key = f'lock:{name}'
        return bool(self.conn.set(name=key, value='set', ex=expire))

    def lock_del(self, name: str) -> None:
        """
        Удаляет блокировку по указанному имени.

        :param name: Имя блокировки.
        """
        key = f'lock:{name}'
        self.conn.delete(key)

    def lock_has(self, name: str) -> bool:
        """
        Проверяет, существует ли блокировка по указанному имени.

        :param name: Имя блокировки.
        :return: True, если блокировка существует, иначе False.
        """
        key = f'lock:{name}'
        return self.conn.exists(key) > 0

    def lock_clear_all(self) -> None:
        """
        Удаляет все блокировки с префиксом 'lock:'.
        """
        keys = self.conn.keys('lock:*')
        if keys:
            self.conn.delete(*keys)
