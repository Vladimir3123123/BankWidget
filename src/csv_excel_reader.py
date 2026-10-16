import logging
import os
from typing import Any

import pandas as pd

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler(
        "logs/csv_excel_reader.log", mode="w", encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def read_csv_file(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    :param file_path: путь к CSV-файлу
    :return: список словарей с транзакциями. Пустой список при ошибке
    """
    logger.debug("Вызвана read_csv_file с путём: %s", file_path)

    try:
        data_frame = pd.read_csv(file_path)
    except FileNotFoundError as error:
        logger.error("CSV-файл не найден: %s. Ошибка: %s", file_path, error)
        return []
    except pd.errors.EmptyDataError as error:
        logger.error("CSV-файл пустой: %s. Ошибка: %s", file_path, error)
        return []
    except pd.errors.ParserError as error:
        logger.error("Ошибка парсинга CSV %s: %s", file_path, error)
        return []

    result = data_frame.to_dict(orient="records")
    logger.info("Успешно прочитано %d записей из %s", len(result), file_path)
    return result


def read_excel_file(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла (.xlsx).

    :param file_path: путь к Excel-файлу
    :return: список словарей с транзакциями. Пустой список при ошибке
    """
    logger.debug("Вызвана read_excel_file с путём: %s", file_path)

    try:
        data_frame = pd.read_excel(file_path, engine="openpyxl")
    except FileNotFoundError as error:
        logger.error("Excel-файл не найден: %s. Ошибка: %s", file_path, error)
        return []
    except ValueError as error:
        logger.error("Ошибка чтения Excel %s: %s", file_path, error)
        return []

    result = data_frame.to_dict(orient="records")
    logger.info("Успешно прочитано %d записей из %s", len(result), file_path)
    return result


if __name__ == "__main__":
    print(read_csv_file("data/transactions.csv"))
    print(read_excel_file("data/transactions_excel.xlsx"))