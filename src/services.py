import datetime
import json
import logging
import os

import pandas as pd

time = datetime.datetime.now()
time_str = time.strftime("%Y-%m-%d")

logs_dr = os.path.join("..", "logs")
os.makedirs(logs_dr, exist_ok=True)

logger = logging.getLogger("services.py")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join("..", "logs/", f"{time_str}-services.log"), "w", encoding="utf-8")
file_formater = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def search_category_and_description(search_str: str):
    """Принимает строку поиска от пользователя
    и возвращает JSON-ответ со всем вхождения этой строки
    в колонки Категория и Описание"""

    logger.info("Запуск функции")
    path_to_file = os.path.join("..", "data", "operations.xlsx")
    if not os.path.exists(path_to_file):
        logger.error("Файл не найден")
        return json.dumps({"error": "Файл с данными не найден"}, indent=4, ensure_ascii=False)

    logger.info("Читаем файл XLSX")
    df = pd.read_excel(path_to_file)
    logger.info("Отсортировываем данные по входной строке")
    group_sort = df[
        (df["Описание"].str.contains(search_str, case=False)) | (df["Категория"].str.contains(search_str, case=False))
    ]
    logger.info("Формируем словари из отобранных данных")
    dict_to = group_sort.to_dict(orient="records")
    json_dumps = json.dumps(dict_to, indent=4, ensure_ascii=False)

    if not dict_to:
        logger.info("Совпадений не найдено")
        return "Ничего не найдено"
    else:
        logger.info("Завершение функции")
        return json_dumps


if __name__ == "__main__":
    print(search_category_and_description("Супермаркеты"))
