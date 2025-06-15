import json
import logging

from src.utils import parse_excel_operations

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs/services.logs", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def finder(data: str) -> list[dict]:
    logger.info("Функция начала выполнение работы")
    transactions = parse_excel_operations()
    result = []
    for transaction in transactions:
        if data in transaction["Категория"]:
            result.append(transaction)
    logger.info("Функция успешно завершена")
    return result
