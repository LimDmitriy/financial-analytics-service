import time
from datetime import date
from functools import wraps
from typing import Any, Callable


def file_log(func):
    """Декоратор для логирования функции"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            message = f"{date.today()}. {func.__name__} - OK. Время выполнения - {end - start:.2f} секунд.\n"
            with open("/Users/dimalim/PycharmProjects/course_project/file_log.txt", "w") as file:
                file.write(message)
        except Exception as e:
            error_type = type(e).__name__
            message = f"{func.__name__} error: {error_type}."
            with open("/Users/dimalim/PycharmProjects/course_project/file_log.txt", "w") as file:
                file.write(message)

        return result

    return wrapper


def log(file_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор для логирования функции, с обязательным параметром"""

    def my_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()
                message = f"{date.today()}. {func.__name__} - OK. Время выполнения - {end - start:.2f} секунд.\n"
            except Exception as e:
                error_type = type(e).__name__
                message = f"{func.__name__} error: {error_type}. Inputs: {args} {kwargs}\n"
                with open(file_name, "w") as file:
                    file.write(message)

                raise

            with open(file_name, "w") as file:
                file.write(message)

            return result

        return wrapper

    return my_decorator
