import logging
from typing import Optional, Type

from pynauriz.utils.redis_manager import RedisManager

logger = logging.getLogger(__name__)


class LockException(BaseException):
    """Исключение, возникающее при попытке выполнить задачу, уже имеющую блокировку."""
    pass


class SingleTaskContextWrapper:
    """
    Обертка для `SingletonTaskContext`, перехватывающая исключение `LockException`.

    Используется для предотвращения падения кода, если блокировка уже установлена.
    """

    def __enter__(self) -> 'SingleTaskContextWrapper':
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback) -> bool:
        """
        Обрабатывает выход из контекста.

        :param exc_type: Тип исключения (если оно возникло).
        :param exc_value: Само исключение.
        :param traceback: Трассировка стека вызовов.
        :return: `True`, если исключение `LockException` было обработано, иначе `False`.
        """
        if exc_type and issubclass(exc_type, LockException):
            return True
        return False


class SingletonTaskContext:
    """
    Контекстный менеджер для выполнения уникальных задач.

    Этот менеджер предотвращает одновременное выполнение одной и той же задачи,
    устанавливая блокировку в Redis.

    Использование:
    ```
    with SingletonTaskContext("task_name"):
        # Код, который должен выполняться только в одном экземпляре
    ```
    """

    def __init__(self, name: str, redis_url: Optional[str] = None):
        """
        Инициализирует контекстный менеджер.

        :param name: Имя блокировки, уникальное для задачи.
        :param redis_url: URL подключения к Redis. Если `None`, используется `redis://localhost:6379/0`.
        """
        self.redis_url = redis_url or "redis://localhost:6379/0"
        self.helper = RedisManager(redis_url=self.redis_url)
        self.name = name

    def __enter__(self) -> 'SingletonTaskContext':
        """
        Вход в контекстный менеджер.

        Проверяет, установлена ли блокировка для данной задачи.
        Если блокировка есть, выбрасывает `LockException`.

        :return: Сам объект `SingletonTaskContext`.
        """
        if self.helper.lock_has(self.name):
            logger.info('Задача "%s" уже выполняется', self.name)
            raise LockException(self.name)

        self.helper.lock_set(self.name)
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback) -> bool:
        """
        Выход из контекста.

        При выходе из блока `with` блокировка снимается.

        :param exc_type: Тип исключения (если возникло).
        :param exc_value: Само исключение.
        :param traceback: Трассировка стека вызовов.
        :return: `False`, чтобы исключение не перехватывалось.
        """
        self.helper.lock_del(self.name)
        return False
