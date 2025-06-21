from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import parse_excel_operations, load_transactions_from_excel, cards, top_transactions, greeting


@patch("src.utils.pd.read_excel")
@patch("src.utils.os.getenv")
def test_parse_excel_operations(mock_getenv, mock_read_excel):
    mock_getenv.return_value = "path/to/file_excel"
    mock_test = pd.DataFrame([{"test": 0, "sample": 0}])
    mock_read_excel.return_value = mock_test
    result = parse_excel_operations()
    expected = [{"test": 0, "sample": 0}]
    assert result == expected


@patch("src.utils.os.getenv", return_value="fake.xlsx")
@patch("src.utils.pd.read_excel", side_effect=FileNotFoundError("Файл не найден"))
def test_parse_excel_operations_raises(mock_read_excel, mock_getenv):
    with pytest.raises(FileNotFoundError):
        parse_excel_operations()


@patch("src.utils.os.getenv")
@patch("src.utils.pd.read_excel")
def test_load_transactions_from_excel(mock_read_excel, mock_getenv):
    mock_getenv.return_value = "path/to/file_excel"
    mock_test = pd.DataFrame([{"test": 0, "sample": 0}])
    mock_read_excel.return_value = mock_test
    result = load_transactions_from_excel()
    pd.testing.assert_frame_equal(result, mock_test)


@pytest.mark.parametrize(
    "hour, expected",
    [
        (7, "Доброе утро"),
        (13, "Добрый день"),
        (19, "Добрый вечер"),
        (1, "Доброй ночи"),
    ],
)
def test_greeting_by_hour(hour, expected):
    fake_datetime = datetime(2025, 6, 22, hour, 0, 0)


@pytest.mark.parametrize(
    "hour, expected",
    [
        (7, "Доброе утро"),
        (13, "Добрый день"),
        (19, "Добрый вечер"),
        (1, "Доброй ночи"),
    ],
)
@patch("src.utils.datetime")
def test_greeting_by_hour(mock_datetime, hour, expected):
    mock_datetime.now.return_value = datetime(2025, 6, 22, hour, 0)
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
    assert greeting() == expected


def test_cards(card):
    result = cards(card)
    assert result == [
        {"last_digit": "5678", "total_spent": 1000.0, "cashback": 100.0},
        {"last_digit": "4321", "total_spent": 250.75, "cashback": 25.08},
    ]


def test_card_empty_transactions():
    result = cards([])
    assert result == []


def test_top_transactions_returns_top_5(transactions_data):
    result = top_transactions(transactions_data)

    assert len(result) == 5
    assert result[0]["amount"] == 5000
    assert result[1]["amount"] == 1200
    assert result[2]["amount"] == 1000
    assert result[3]["amount"] == 700
    assert result[4]["amount"] == 300


def test_cards_missing_fields():
    transactions = [{"Сумма операции с округлением": 500}]  # без номера карты
    result = cards(transactions)
    assert result == [{"last_digit": "", "total_spent": 500, "cashback": 50.0}]
