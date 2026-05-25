import datetime
import json
import logging
import os.path

import pandas as pd  # type: ignore
import requests

time = datetime.datetime.now()
time_str = time.strftime("%Y-%m-%d")

# Настройка логов
logger = logging.getLogger('views.py')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join('..', 'logs/', f'{time_str}-views.log'), 'w', encoding='utf-8')
file_formater = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def main_view(time_now: str) -> json:
    """Принимает строку в формате ГГ-ММ-ДД Ч:М:С
    возвращает JSON-ответ"""

    logger.info("Запуск функции")
    # Итоговый словарь
    result_dict = {
        "greeting": None,
        "cards": None,
        "top_transactions": None,
        "currency_rates": None,
        "stock_prices": None,
    }

    # Проверяем валидность строки даты
    try:
        # Достаем строку, чтобы узнать который час
        get_hour = time_now.split()[1][0:2]
        # Добавляем приветствие в зависимости от времени суток
        result_dict["greeting"] = (
            "Доброе утро"
            if 5 <= int(get_hour) <= 12
            else (
                "Добрый день"
                if 13 <= int(get_hour) <= 16
                else "Добрый вечер" if 17 <= int(get_hour) <= 22 else "Доброй ночи"
            )
        )
        logger.info("Добавляем приветствие в зависимости от времени суток")
    # Если поступили не валидные данные, то записываем строку "Здравствуйте" в result_dict["greeting"]
    except Exception as ex:
        logger.error(f"Ошибка входной строки {type(ex)}")
        result_dict["greeting"] = "Здравствуйте"

    try:
        # Читаем XLSX-файл
        df = pd.read_excel(os.path.join("..", "data", "operations.xlsx"))
        # Выбираем только те сумы где есть "-" трата
        sorted_sum = df[df["Сумма операции"] < 0]
        # Формируем группу из номеров карт и суммируем все потраченные суммы
        group_sum = sorted_sum.groupby("Номер карты")["Сумма операции"].sum().reset_index()
        # Отсортировываем данные по 5 самым большим тратам
        group_max_sum = sorted_sum.sort_values("Сумма операции")[:5][
            ["Сумма операции", "Категория", "Дата платежа", "Описание"]
        ]

        # Добавляем данные о картах и суммах в итоговый словарь
        result_dict["cards"] = [
            {
                "last_digits": str(row["Номер карты"]).lstrip("*"),
                "total_spent": float(str(row["Сумма операции"]).lstrip("-")),
                "cashback": float(str(row["Сумма операции"]).lstrip("-")) / 100,
            }
            for _, row in group_sum.iterrows()
        ]
        logger.info("Добавляем информацию в итоговый словарь в result_dict[cards] ")

        # Добавляем топовые транзакции в итоговый словарь
        result_dict["top_transactions"] = [
            {
                "data": row["Дата платежа"],
                "amount": float(str(row["Сумма операции"]).lstrip("-")),
                "category": row["Категория"],
                "description": row["Описание"],
            }
            for _, row in group_max_sum.iterrows()
        ]
        logger.info("Добавляем информацию в итоговый словарь в result_dict[top_transactions]")
    except FileNotFoundError as ex:
        logger.error(f"Файл XLSX не найден {ex}")

    # Проверяем что файл есть по указанному пути
    try:
        # Читаем файл и достаем от туда запрос пользователя
        with open(os.path.join("../user_settings.json"), "r") as file_json:
            options_list = json.load(file_json)
        # Валюта, которую указал юзер
        currency_user = options_list["user_currencies"]
        # Акции которые указал юзер
        stock_user = options_list["user_stocks"]
        logger.info("Читаем файл JSON с параметрами юзера")

        # Запрос к АПИ для данных о курсе валют с ЦБ РФ
        response_currency = requests.get(url="https://www.cbr-xml-daily.ru/daily_json.js", timeout=10)
        logger.info("Запрос к внешнему API курса валют ЦБ РФ")
        # Если статус код == 200, то записываем данные о курсе валют в result_dict
        if response_currency.status_code == 200:
            logger.info("Добавление данных в result_dict[currency_rates] ")
            json_response = response_currency.json()
            result_dict["currency_rates"] = [
                {"currency": code, "rate": json_response.get("Valute", "Валюта не найдена")[code]["Value"]}
                for code in currency_user
            ]
        # Если статус код != 200, то записываем сообщение, что курс валют временно не доступен в result_dict
        else:
            result_dict["currency_rates"] = [{"currency": "Временно недоступно", "rate": "Временно не доступно"}]

        # Создаем временный список для хранения полученных словарей с данными об акциях
        temporary_list = []
        # Запуск цикла по акциям которые хотел узнать пользователь
        for stock in stock_user:
            # Обращение к внешнему АПИ с именем акции
            url_stock = (f"https://financialmodelingprep.com/stable/profile?symbol={stock}"
                         f"&apikey=LLPSf9IHTTHjAbZDTfRN9lqtUdv2uUem")
            logger.info(f"Обращение к API для информации об акциях {stock}")
            response_stock = requests.get(url=url_stock, timeout=10)
            # Если статус код == 200, преобразуем полученные данные в json
            if response_stock.status_code == 200:
                json_stock = response_stock.json()
                # Добавляем данные в, временный список temporary_list
                temporary_list += [{"stock": x["symbol"], "price": x["price"]} for x in json_stock]
        # Если список temporary_list не пустой, то добавляем данные в итоговый словарь
        if temporary_list:
            logger.info("Записываем данные в итоговый словарь result_dict[stock_prices] = temporary_list ")
            result_dict["stock_prices"] = temporary_list
        # Если список temporary_list пуст, то в "stock" и "price" Записывается строка о временной недоступности
        else:
            result_dict["stock_prices"] = [{"stock": "Временно не доступно", "price": "Временно не доступно"}]
    except FileNotFoundError as ex:
        logger.error(f"Файл JSON не найден {ex}")
    except requests.exceptions.RequestException as ex:
        logger.error(f"Ошибка запроса: {ex}")

    logger.info("Завершение функции")
    return json.dumps(result_dict, indent=4, ensure_ascii=False)
