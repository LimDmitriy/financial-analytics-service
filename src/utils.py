import os
from datetime import datetime
from typing import Any

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def parse_excel_operations() -> list[dict[Any, Any]]:
    """Функция для считывания финансовых операций из EXCEL, выдает список словарей"""
    file_path = os.getenv("PATH_EXCEL")
    df = pd.read_excel(file_path).fillna("")
    return df.to_dict(orient="records")


def load_transactions_from_excel() -> pd.DataFrame:
    """Функция для считывания финансовых операций из EXCEL"""
    file_path = os.getenv("PATH_EXCEL")
    df = pd.read_excel(file_path)
    return df


def greeting() -> str:
    """Функция приветсвия в зависимости от текущего времени суток"""
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def cards(transactions: list[dict]) -> list[dict[str, Any]]:
    """Функция возвращает последние 4 цифры карты, общую сумму расхода, кэшбэк"""
    result = []
    for transaction in transactions:
        card_number = transaction.get("Номер карты", "")
        last_digit = card_number[-4:]
        amount = transaction.get("Сумма операции с округлением")
        cashback = round(amount * 0.1, 2)
        result.append({"last_digit": last_digit, "total_spent": amount, "cashback": cashback})
    return result


def top_transactions(transactions: list[dict]) -> list[dict]:
    """Функция возвращает топ 5 операций"""
    sorted_transactions = sorted(transactions, key=lambda t: t.get("Сумма операции с округлением", ""))
    top_5 = sorted_transactions[-5:]
    result = []
    for t in top_5:
        result.append(
            {
                "date": t.get("Дата операции", "")[0:10],
                "amount": t.get("Сумма операции с округлением", 0),
                "category": t.get("Категория", ""),
                "description": t.get("Описание", ""),
            }
        )
    return result
