import csv
import datetime
import logging
import os
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

time = datetime.datetime.now()
time_str = time.strftime("%Y-%m-%d")

logger = logging.getLogger("report.py")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join("..", "logs/", f"{time_str}-report.log"), "w", encoding="utf-8")
file_formate = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formate)
logger.addHandler(file_handler)


def records(name_file: Optional[str]= None):
    def report_decorator(func):
        def wrapper(*arg, **kwargs):
            if name_file:
                str_name_file = f"{name_file}-{time_str}"
            else:
                str_name_file = f"report-{time_str}"
            result = func(*arg, **kwargs)
            result.to_csv(f"../data/{str_name_file}.csv", index=False, encoding="utf-8")
        return wrapper
    return report_decorator


@records()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за
    последние три месяца (от переданной даты)"""

    logger.info("Запуск функции")
    if date:
        logger.info("Превращаем переданную дату в объект datetime")
        start_date = datetime.datetime.strptime(date, "%d.%m.%Y")
    else:
        logger.info("Дата не передана в функцию, используем текущую дату")
        start_date = datetime.datetime.now()
    end_date = start_date - relativedelta(months=3)

    logger.info("Отсортировываем DF по всем поступившим критериям")
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    mask = (
        (transactions["Дата операции"] >= end_date)
        & (transactions["Дата операции"] <= start_date)
        & (transactions["Категория"] == category)
    )
    logger.info("Проверяем DF на то пуст ли он")
    filtered = transactions.loc[mask, ["Категория", "Сумма операции"]]
    if filtered.empty:
        logger.info("Список пуст")
        logger.info("Завершение функции")
        return pd.DataFrame({"Результат": ["Ничего не найдено"]})
    logger.info("Список успешно отсортирован")
    logger.info("Успешное завершение функции")
    result = filtered.groupby("Категория", as_index=False)["Сумма операции"].sum()
    return result
