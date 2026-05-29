import pytest
import pandas as pd


# fixture для get_info_tabel
@pytest.fixture
def data_set_positive():
    test_data = pd.DataFrame({"Номер карты": ["*1234"], "Сумма операции": [-1000.0]})
    return test_data


@pytest.fixture
def return_positive_result():
    return [{"last_digits": "1234", "total_spent": 1000.0, "cashback": 10.0}]


# fixture для top_five_transactions
@pytest.fixture
def data_set_top():
    return pd.DataFrame(
        {
            "Дата операции": ["21.03.2019 17:01:37"],
            "Сумма операции": [-1000.0],
            "Категория": ["Магазин"],
            "Описание": ["SexShop"],
        }
    )


@pytest.fixture
def result_top_set():
    return [{"date": "21.03.2019 17:01:37", "amount": 1000.0, "category": "Магазин", "description": "SexShop"}]

@pytest.fixture
def test_data_for_spending_by_category():
    return pd.DataFrame({"Дата операции" : ["20.05.2020", "20.04.2020"],
                         "Категория" : ["Супермаркеты", "Супермаркеты"],
                         "Сумма операции" : [1000, 1500]})

@pytest.fixture
def done_data_for_data_for_spending_by_category():
    return pd.DataFrame({"Категория" : ["Супермаркеты"], "Сумма операции" : [2500]})
