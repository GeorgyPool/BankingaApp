import datetime
import logging
import os

import pandas as pd  # typing ignore

time = datetime.datetime.now()
time_str = time.strftime("%Y-%m-%d")

logs_dir = os.path.join("..", "logs")
os.makedirs(logs_dir, exist_ok=True)

logger = logging.getLogger("get_info_tabel")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join("..", "logs", f"{time_str}-get_info_tabel.log"), "w", encoding="utf-8")
file_formater = logging.Formatter("%(asctime)s %(name)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def get_info_of_cards() -> list[dict]:
    """Читает JSON-файл и возвращает список словарей
    с информацией о банковских операциях"""

    logger.info("Запуск функции")

    logger.info("Проверка существования файла")
    path = os.path.join("..", "data", "operations.xlsx")
    if os.path.exists(path):
        logger.info("Файл найден")

        logger.info("Читаем файл, преобразуем его в DataFrame")
        df = pd.read_excel(path)
        logger.info("Сортируем по тратам")
        card_spending = df[df["Сумма операции"] < 0]
        logger.info("Группируем по номерам карт и сумме всех трат")
        group_num_card = card_spending.groupby("Номер карты").agg({"Сумма операции": "sum"}).reset_index()
        logger.info("Записываем все данные из сформированной группы в список словарей")
        cards_info = [
            {
                "last_digits": str(x["Номер карты"]).lstrip("*"),
                "total_spent": float(str(x["Сумма операции"]).lstrip("-")),
                "cashback": float(str(x["Сумма операции"] / 100).lstrip("-")),
            }
            for _, x in group_num_card.iterrows()
        ]
        logger.info("Возвращаем список словарей")
        logger.info("Завершение функции")
        return cards_info
    else:
        logger.info("Файл не найден, Завершение функции")
        card_info = [{"Файл": "Не найден"}]
        return card_info


def top_five_transactions() -> list[dict]:
    """Читает JSON-файл и возвращает
    топ пяти платежей от самой большой суммы к меньшей
    с описанием и категорией list[dict]"""

    logger.info("Запуск функции")
    path = os.path.join("..", "data", "operations.xlsx")
    logger.info("Проверка что файл существует по указанному пути")
    if os.path.exists(path):
        logger.info("Файл существует")
        df = pd.read_excel(path)
        logger.info("Отсортировываем по транзакциям ")
        spending = df[df["Сумма операции"] < 0].sort_values("Сумма операции").head()

        logger.info("Записываем данные в итоговый список")
        top_transactions = [
            {
                "date": x["Дата операции"],
                "amount": float(str(x["Сумма операции"]).lstrip("-")),
                "category": x["Категория"],
                "description": x["Описание"],
            }
            for _, x in spending.iterrows()
        ]
        logger.info("Успешная запись")
        logger.info("Завершение функции")
        return top_transactions
    else:
        logger.info("Файл не найден")
        return [{"Файл": "Не найден"}]
