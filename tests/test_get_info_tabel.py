from unittest.mock import patch

from src.get_info_tabel import get_info_of_cards, top_five_transactions


# Проверка get_info_of_cards на позитивный вызов функции
@patch("os.path.exists")
@patch("pandas.read_excel")
def test_get_info_of_cards_is_positive(mock_read_excel, mock_exists, data_set_positive, return_positive_result):

    mock_exists.return_value = True
    mock_read_excel.return_value = data_set_positive

    result = get_info_of_cards()
    assert result == return_positive_result
    mock_read_excel.assert_called_once()


# Проверка функции get_info_of_cards на отсутствие файла
@patch("os.path.exists")
def test_get_info_of_cards_not_file(mock_os):
    mock_os.return_value = False
    result = get_info_of_cards()
    assert result == [{"Файл": "Не найден"}]


# Проверка top_five_transactions на положительный результат
@patch("os.path.exists")
@patch("pandas.read_excel")
def test_top_five_transactions_is_positive(moc_pd, mock_os, data_set_top, result_top_set):
    mock_os.return_value = True
    moc_pd.return_value = data_set_top
    result = top_five_transactions()
    assert result == result_top_set
    moc_pd.assert_called_once()


# Проверка top_five_transactions на отсутствие файла
@patch("os.path.exists")
def test_top_five_transactions_is_not_file(mock_os):
    mock_os.return_value = False
    result = top_five_transactions()
    assert result == [{"Файл": "Не найден"}]
