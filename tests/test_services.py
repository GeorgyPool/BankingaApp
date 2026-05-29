from unittest.mock import patch

import pandas as pd

from src.services import search_category_and_description

# Проверка search_category_and_description на позитивный исход
@patch("os.path.exists")
@patch("pandas.read_excel")
@patch("json.dumps")
def test_search_category_and_description_is_positive(mock_js, mock_pd, mock_os):
    mock_os.return_value = True

    mock_pd.return_value = pd.DataFrame({"Описание" : ["tests"], "Категория" : ["tests"]})
    mock_js.return_value = {"Описание" : "tests", "Категория" : "tests"}
    result = search_category_and_description("tests")
    assert result == {"Описание" : "tests", "Категория" : "tests"}
    mock_os.assaert_called_once()
    mock_pd.assert_called_once()
    mock_js.assert_called_once()

# Проверка search_category_and_description на отсутствие файла
@patch("os.path.exists")
@patch("json.dumps")
def test_search_category_and_description(mock_js, mock_os):
    mock_os.return_value = False
    mock_js.return_value = {"error": "Файл с данными не найден"}
    result = search_category_and_description("tests")
    assert result == {"error": "Файл с данными не найден"}
    mock_os.assert_called_once()
    mock_js.assert_called_once()

# Проверка search_category_and_description на пустую сортировку
@patch("os.path.exists")
@patch("pandas.read_excel")
def test_search_category_and_description_not_str(moc_pd, mock_os):
    mock_os.return_value = True
    moc_pd.return_value = pd.DataFrame({"Описание" : ["test"], "Категория" : ["test"]})
    result = search_category_and_description("tuk")
    assert result == "Ничего не найдено"