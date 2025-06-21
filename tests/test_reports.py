import pandas as pd
import pytest
from pandas import Timestamp

from src.reports import spending_by_category


def test_spending_by_category(data):

    result = spending_by_category(data, "Еда", "2024-05-10 10:00:00")
    assert result == [
        {"Дата операции": Timestamp("2024-03-01 12:00:00"), "Категория": "Еда", "Сумма": 500},
        {"Дата операции": Timestamp("2024-05-10 10:00:00"), "Категория": "Еда", "Сумма": 700},
    ]


@pytest.mark.parametrize(
    "transactions, category, date, expected_exception",
    [
        ("not_dataframe", "Еда", "2024-06-01 00:00:00", TypeError),
        (pd.DataFrame(), "Еда", "06-01-2024", ValueError),
    ],
)
def test_spending_by_category_exceptions(transactions, category, date, expected_exception):
    with pytest.raises(expected_exception):
        spending_by_category(transactions, category, date)


def test_spending_by_category_empty_transaction(data):
    result = spending_by_category(data, "Тест", "2025-06-22 00:00:00")
    assert result == []


def test_spending_by_category_empty_date(data):
    result = spending_by_category(data, "Еда")
    assert result == []
