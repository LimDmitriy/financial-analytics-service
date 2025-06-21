import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Hashable

import pandas as pd

from src.decorators import log
from src.utils import load_transactions_from_excel

data = load_transactions_from_excel()

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs/reports.logs", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


@log("/Users/dimalim/PycharmProjects/course_project/log.txt")
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> list[dict[Hashable, Any]]:
    """Функция фильтрует транзакции по категории и дате (за последние 90 дней до указанной даты)"""
    logger.info("Функция начала выполнение работы")
    if not isinstance(transactions, pd.DataFrame):
        logger.error("Ошибка: {transactions} не являeтся DataFrame")
        raise TypeError("{transactions} должен быть pandas DataFrame")
    try:
        date_str = datetime.strptime(date, "%Y-%m-%d %H:%M:%S") if date else datetime.now()
    except ValueError as e:
        logger.error(f"Неверный формат даты: {date}. Ожидается '%Y-%m-%d %H:%M:%S'")
        raise e

    target_date = date_str - timedelta(days=90)

    try:
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    except Exception as e:
        logger.error("Ошибка при конвертации 'Дата операции' в datetime")
        raise e

    filtred = transactions[
        (transactions["Дата операции"] >= target_date)
        & (transactions["Дата операции"] <= date_str)
        & (transactions["Категория"] == category)
    ]
    logger.info("Функция успешно завершена")
    return filtred.to_dict(orient="records")
