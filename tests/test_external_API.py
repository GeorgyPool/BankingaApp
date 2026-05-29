from requests.exceptions import Timeout
from unittest.mock import patch, mock_open
from src.external_API import response_exchange_rate, response_stocks

# Тесты для response_exchange_rate
# Проверка на позитивный исход функции response_exchange_rate
@patch("os.path.exists")
@patch("builtins.open", mock_open(read_data='{"user_currencies": ["USD"]}'))
@patch("requests.get")
def test_response_exchange_rate_is_positive(mock_requests, mock_os):
    mock_os.return_value = True
    mock_response = mock_requests.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Valute": {
            "USD": {
                "CharCode": "USD",
                "Value": 70.9012
            }
        }
    }

    result = response_exchange_rate()
    expected = [{"currency": "USD", "rate": 70.9012}]
    assert result == expected
    mock_requests.assert_called_once()
    mock_os.assert_called_once()

# Проверка на отсутствие файла
@patch("os.path.exists")
def tests_response_exchange_rate_not_file(mock_os):
    mock_os.return_value = False
    result = response_exchange_rate()
    assert result == [{"Файл": "Не найден"}]
    mock_os.assert_called_once()

# Проверка на то что статус код response_exchange_rate не равен 200
@patch("os.path.exists")
@patch("builtins.open", mock_open(read_data='{"user_currencies": ["USD"]}'))
@patch("requests.get")
def test_response_exchange_rate_fail_status_code(mock_requests, mock_os):
    mock_os.return_value = True
    mock_response = mock_requests.return_value
    mock_response.return_value = 404
    result = response_exchange_rate()
    assert result == [{"Ошибка": "Ошибка запроса к API"}]
    mock_os.assert_called_once()
    mock_requests.assert_called_once()

# Тесты для response_stocks
# Тест на позитивный исход response_stocks
@patch("os.path.exists")
@patch("builtins.open", mock_open(read_data='{"user_stocks": ["GOOGL"]}'))
@patch("requests.get")
def test_response_stocks_is_positive(mock_requests, mock_os):
    mock_os.return_value = True

    mock_response = mock_requests.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = [{"symbol" : "GOOGL", "price" : 20}]
    result = response_stocks()
    assert  result == [{"stock" : "GOOGL", "price" : 20}]
    mock_requests.assert_called_once()
    mock_os.assert_called_once()

# Тест response_stocks на отсутствие файла с пользовательскими настройками
@patch("os.path.exists")
def test_response_stocks_not_file(mock_os):
    mock_os.return_value = False
    result = response_stocks()
    assert result == [{"Ошибка" : "Файл не найден"}]
    mock_os.assert_called_once()

# Тест response_stocks на слишком долгий ответ по API
@patch("os.path.exists")
@patch("builtins.open", mock_open(read_data='{"user_stocks": ["GOOGL"]}'))
@patch("requests.get")
def test_response_stocks_long_time(mock_requests, mock_os):
    mock_os.return_value = True
    mock_requests.side_effect = Timeout("Connection timeout or network error")
    result = response_stocks()
    assert result == [{"Ошибка" : "Долгий ответ от API"}]
    mock_os.assert_called_once()
    mock_requests.assert_called_once()