import functools
from collections.abc import Callable
from typing import Any


def log(filename: str | None = None) -> Callable:
    """Декоратор для логирования работы функции.

    Логирует имя функции и результат при успешном выполнении,
    либо имя функции, тип ошибки и входные параметры — при ошибке.

    :param filename: имя файла для записи логов. Если не задан,
        логи выводятся в консоль.
    :return: декоратор, оборачивающий функцию
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                message = (
                    f"{func.__name__} error: {type(error).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write_log(message, filename)
                raise
            else:
                message = f"{func.__name__} ok"
                _write_log(message, filename)
                return result

        return wrapper

    return decorator


def _write_log(message: str, filename: str | None) -> None:
    """Записывает сообщение в файл или выводит в консоль.

    :param message: текст сообщения для логирования
    :param filename: имя файла. Если None — вывод в консоль
    """
    if filename is None:
        print(message)
    else:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(message + "\n")