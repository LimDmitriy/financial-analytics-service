import json
import logging
import os
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv


from src.utils import parse_excel_operations

load_dotenv()


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs/views.logs", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


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


with open("../user_settings.json", "r", encoding="utf-8") as f:
    config_data = json.load(f)

user_currencies = config_data.get("user_currencies", "")  # Курсы валют
user_stocks = config_data.get("user_stocks", "")  # Акции


def currency_rates(currencies: list) -> list[dict]:
    """Функция для вывода курса с помощью API"""
    api_key = os.getenv("API_KEY_CURRENCY")
    to_currency = ",".join(currencies)
    url = f"http://api.currencylayer.com/live?access_key={api_key}&currencies={to_currency}"
    response = requests.get(url)
    data = response.json()
    quotes = data["quotes"]
    return [
        {"cyrrency": "RUB", "rate": round(quotes["USDRUB"], 2)},
        {"cyrrency": "EUR", "rate": round(quotes["USDEUR"], 2)},
    ]


def stocks(stocks: list) -> list[dict]:
    """Функция для вывода курса акций"""
    api_key = os.getenv("API_KEY_STOCKS")
    url = f"https://finnhub.io/api/v1/quote"
    result = []
    for stock in stocks:
        params = {"symbol": stocks, "token": api_key}
        response = requests.get(url, params=params)
        data = response.json()
        result.append({"stock": stock, "price": data["c"]})
    return result


def home_page(date: str) -> dict:
    logger.info("Функция начала выполнение работы")
    target_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    target_mounth = target_date.month
    target_year = target_date.year
    transactions = parse_excel_operations()
    filtred_transactions = []
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if transaction_date.year == target_year and transaction_date.month == target_mounth:
            filtred_transactions.append(transaction)

    result = {
        "greeting": greeting(),
        "cards": cards(filtred_transactions),
        "top_transactions": top_transactions(filtred_transactions),
        "currency_rates": currency_rates(user_currencies),
        "stock_prices": stocks(user_stocks),
    }
    logger.info("Функция успешно завершена")
    return result


print(home_page("2021-12-01 13:33:33"))
