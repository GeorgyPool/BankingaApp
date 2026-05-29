import datetime
import json

from src.external_API import response_exchange_rate, response_stocks
from src.get_info_tabel import get_info_of_cards, top_five_transactions

time = datetime.datetime.now()
time_str = time.strftime("%Y-%m-%d %H:%M:%S")


def main_view(time_now: str) -> json:
    """Главная функции"""

    result_dict = {
        "greeting": None,
        "cards": None,
        "top_transactions": None,
        "currency_rates": None,
        "stock_prices": None,
    }

    split_time = int(time_now.split()[1][:2])
    result_dict["greeting"] = (
        "Доброе утро"
        if 6 <= split_time <= 11
        else "Добрый день" if 12 <= split_time <= 17 else "Добрый вечер" if 18 <= split_time <= 22 else "Доброй ночи"
    )

    result_dict["cards"] = get_info_of_cards()
    result_dict["top_transactions"] = top_five_transactions()
    result_dict["currency_rates"] = response_exchange_rate()
    result_dict["stock_prices"] = response_stocks()

    return json.dumps(result_dict, indent=4, ensure_ascii=False)


print(main_view(time_str))
