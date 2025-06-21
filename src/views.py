import json
import logging
import os
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv

from src.utils import cards, greeting, parse_excel_operations, top_transactions

load_dotenv()


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs/views.logs", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


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
    url = "https://finnhub.io/api/v1/quote"
    result = []
    for stock in stocks:
        params = {"symbol": stocks, "token": api_key}
        response = requests.get(url, params=params)
        data = response.json()
        result.append({"stock": stock, "price": data["c"]})
    return result


def home_page(date: str) -> dict[str, Any]:

    logger.info("Функция home_page начала выполнение работы")
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logger.error("Неверный формат даты: {date}. Ожидается 'YYYY-MM-DD HH:MM:SS'")
        raise e

    try:
        transactions = parse_excel_operations()
    except Exception as e:
        logger.error("Ошибка при получении транзакции")
        raise e

    filtered_transactions = []
    for transaction in transactions:
        try:
            transaction_date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
            if transaction_date.year == target_date.year and transaction_date.month == target_date.month:
                filtered_transactions.append(transaction)
        except Exception as e:
            logger.error("Ошибка даты")
            raise e

    result = {
        "greeting": greeting(),
        "cards": cards(filtered_transactions),
        "top_transactions": top_transactions(filtered_transactions),
        "currency_rates": currency_rates(user_currencies),
        "stock_prices": stocks(user_stocks),
    }
    logger.info("Функция успешно завершена")
    return result


print(home_page("2021-12-01 13:33:33"))
