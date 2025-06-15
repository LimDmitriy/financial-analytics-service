import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

from src.utils import load_transactions_from_excel

data = load_transactions_from_excel()

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs/reports.logs", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def file_log(func):
    """Декоратор для логирования функции"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        message = f"{func.__name__} - {result}\n"
        with open("/Users/dimalim/PycharmProjects/course_project/file_log.txt", "a") as file:
            file.write(message)

        return result

    return wrapper


def log(file_name: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор для логирования функции"""

    def my_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} - {result}. OK\n"
            except Exception as e:
                error_type = type(e).__name__
                message = f"{func.__name__} error: {error_type}. Inputs: {args} {kwargs}\n"
                if file_name:
                    with open(file_name, "a") as file:
                        file.write(message)
                else:
                    print(message)
                raise
            if file_name:
                with open(file_name, "a") as file:
                    file.write(message)
            else:
                print(message)
            return result

        return wrapper

    return my_decorator


@log("/Users/dimalim/PycharmProjects/course_project/file_log.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> list[Any]:
    logger.info("Функция начала выполнение работы")
    if date:
        date_str = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        date_str = datetime.now()

    target_date = date_str - timedelta(days=90)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    result = transactions[
        (transactions["Дата операции"] >= target_date)
        & (transactions["Дата операции"] <= date_str)
        & (transactions["Категория"] == category)
    ]
    logger.info("Функция успешно завершена")
    return result.to_dict(orient="records")


print(spending_by_category(data, "Супермаркеты", "2021-11-11 22:22:22"))
