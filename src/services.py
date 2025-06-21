import logging

from src.utils import parse_excel_operations

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("/Users/dimalim/PycharmProjects/course_project/logs/reports.logs", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def finder(data: str) -> list[dict]:
    """Функция для поиска транзакций по заданой строке"""
    logger.info("Функция начала выполнение работы")
    if not isinstance(data, str):
        logger.error("Ошибка: Входные данные должны быть строкой.")
        raise TypeError("{data} не является строкой")
    try:
        transactions = parse_excel_operations()
        result = [t for t in transactions if data in t.get("Категория", "")]
        logger.info("Функция успешно завершена")
        return result
    except Exception as e:
        logger.error("Ошибка при поиске транзакций")
        raise e
