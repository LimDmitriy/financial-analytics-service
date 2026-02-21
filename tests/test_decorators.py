from datetime import date
from unittest.mock import mock_open, patch

from src.decorators import file_log, log


@patch("src.decorators.open", new_callable=mock_open)
@patch("src.decorators.date")
@patch("src.decorators.time")
def test_file_log_success(mock_time, mock_date, mock_file):
    mock_date.today.return_value = "2025-06-22"
    mock_time.time.side_effect = [100.0, 101.5]  # имитируем 1.5 секунды работы

    @file_log
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5

    mock_file.assert_called_with("/Users/dimalim/PycharmProjects/course_project/file_log.txt", "w")

    handle = mock_file()
    handle.write.assert_called_once_with("2025-06-22. add - OK. Время выполнения - 1.50 секунд.\n")


@patch("src.decorators.open", new_callable=mock_open)
@patch("src.decorators.date")
@patch("src.decorators.time")
def test_file_log_success(mock_time, mock_date, mock_file):
    mock_date.today.return_value = date(2025, 6, 22)
    mock_time.time.side_effect = [100.0, 101.5]  # имитируем 1.5 секунды работы

    @log("/Users/dimalim/PycharmProjects/course_project/log.txt")
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5

    mock_file.assert_called_with("/Users/dimalim/PycharmProjects/course_project/log.txt", "w")

    handle = mock_file()
    handle.write.assert_called_once_with("2025-06-22. add - OK. Время выполнения - 1.50 секунд.\n")
