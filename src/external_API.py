import datetime
import json
import logging
import os

import requests

time = datetime.datetime.now()
time_str = time.strftime("%Y-%m-%d")

logs_dir = os.path.join("..", "logs")
os.makedirs(logs_dir, exist_ok=True)

logger = logging.getLogger("external_API")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join("..", "logs", f"{time_str}-external_API.log"), "w", encoding="utf-8")
file_formater = logging.Formatter("%(asctime)s %(name)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def response_exchange_rate() -> list[dict]:
    """Обращается к внешнему API ЦБ РФ для получения
    данных о курсе валют который указал пользователь"""

    logger.info("Запуск функции")
    path = os.path.join("..", "user_settings.json")
    logger.info("Проверка существует ли файл по указанному пути")
    if os.path.exists(path):
        logger.info("Файл найден и преобразован в строку python")
        with open(path, "r") as file_json:
            user_settings = json.load(file_json)
    else:
        logger.info("Файл не найден")
        return [{"Файл": "Не найден"}]
    logger.info("Достаем валюту которую указ пользователь")
    user_currencies = user_settings["user_currencies"]
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    logger.info("Запрашиваем у внешнего API ЦБ РФ информацию о курсе валют")
    try:
        response = requests.get(url=url, timeout=20)
        if response.status_code == 200:
            logger.info("Запрос прошел успешно записываем полученные данный в список")
            rate = response.json()
            currencies_rate = [
                {"currency": rate["Valute"][x]["CharCode"], "rate": rate["Valute"][x]["Value"]}
                for x in user_currencies
            ]
            logger.info("Завершение функции")
            return currencies_rate
        else:
            logger.info("Ошибка запроса к внешнему API")
            return [{"Ошибка": "Ошибка запроса к API"}]
    except requests.exceptions.RequestException:
        return [{"Ошибка": "Ошибка запроса к API"}]


def response_stocks() -> list[dict]:
    """Читает JSON-файл и возвращает ценны на акции которые указал
    пользователь с помощью requests.get"""

    logger.info("Запуск функции")
    path = os.path.join("..", "user_settings.json")
    logger.info("Проверка наличие файла по указанному пути")
    if os.path.exists(path):
        logger.info("Файл найден, читаем его и преобразуем в строку python")
        with open(path, "r") as file_stocks:
            user_settings = json.load(file_stocks)["user_stocks"]
    else:
        logger.info("Файл не найден")
        return [{"Ошибка": "Файл не найден"}]

    result_stocks = []
    logger.info("Запускаем цикл для поиска акций по API")
    for stock in user_settings:
        url = (
            f"https://financialmodelingprep.com/stable/profile?symbol={stock}&apikey=LLPSf9IHTTHjAbZDTfRN9lqtUdv2uUem"
        )
        try:
            logger.info("Проверка что API равен статус коду 200")
            response = requests.get(url=url, timeout=30)
            if response.status_code == 200:
                logger.info("Статус код верен преобразуем ответ от API")
                get = response.json()[0]
                result_stocks.append({"stock": get["symbol"], "price": get["price"]})
        except requests.RequestException:
            logger.error("Ошибка: долгое ожидание от API")
            return [{"Ошибка": "Долгий ответ от API"}]
    logger.info("Успешно, завершение работы функции")
    return result_stocks
