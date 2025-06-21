from unittest.mock import patch

import pytest

from src.services import finder


@patch("src.services.parse_excel_operations")
def test_finder_returns_empty_list(mock_parse, mock_transactions):
    mock_parse.return_value = mock_transactions
    result = finder("Здоровье")
    assert result == []


def test_finder_raises_type_error():
    with pytest.raises(TypeError):
        finder(123)


@patch("src.services.parse_excel_operations")
def test_finder_returns_matching(mock_parse):
    mock_parse.return_value = [
        {"Категория": "Еда", "Сумма": 100},
        {"Категория": "Развлечения", "Сумма": 200},
        {"Категория": "Еда и напитки", "Сумма": 150},
    ]

    result = finder("Еда")

    assert result == [
        {"Категория": "Еда", "Сумма": 100},
        {"Категория": "Еда и напитки", "Сумма": 150},
    ]
