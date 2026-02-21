from unittest.mock import patch

from src.views import currency_rates, stocks


@patch("src.views.os.getenv")
@patch("src.views.requests.get")
def test_currency_rates(mock_get, mock_getenv):
    mock_getenv.return_value = "fake_api_key"
    mock_get.return_value.json.return_value = {"quotes": {"USDRUB": 74.1234, "USDEUR": 0.8456}}

    result = currency_rates(["RUB", "EUR"])
    assert result == [
        {"cyrrency": "RUB", "rate": 74.12},
        {"cyrrency": "EUR", "rate": 0.85},
    ]


@patch("src.views.os.getenv")
@patch("src.views.requests.get")
def test_stocks(mock_get, mock_getenv):
    mock_getenv.return_value = "fake_api_key"
    mock_get.return_value.json.return_value = {"c": 123.45}

    result = stocks(["AAPL", "GOOGL"])
    assert result == [
        {"stock": "AAPL", "price": 123.45},
        {"stock": "GOOGL", "price": 123.45},
    ]
