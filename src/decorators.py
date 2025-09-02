import functools
import sys
from typing import Any, Callable, Optional, TextIO


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций. Регистрирует:
    - Успешное выполнение: имя функции и результат
    - Ошибки: имя функции, тип ошибки и входные параметры

    :param filename: Имя файла для логирования (None - вывод в консоль)
    :return: Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Форматирование входных параметров
            params = f"({', '.join(map(str, args))}"
            if kwargs:
                params += f", {', '.join(f'{k}={v}' for k, v in kwargs.items())}"
            params += ")"

            log_stream: TextIO
            close_stream = False

            try:
                if filename:
                    log_stream = open(filename, "a", encoding="utf-8")
                    close_stream = True
                else:
                    log_stream = sys.stdout

                try:
                    result = func(*args, **kwargs)
                    log_stream.write(f"{func.__name__} ok\n")
                    return result

                except Exception as e:
                    log_stream.write(f"{func.__name__} error: {type(e).__name__}. Inputs: {params}\n")
                    raise

            finally:
                if close_stream:
                    log_stream.close()

        return wrapper

    return decorator
