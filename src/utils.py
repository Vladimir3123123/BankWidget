import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """Загружает список транзакций из JSON-файла.

    Если файл не найден, пустой, содержит не список или невалидный JSON —
    возвращает пустой список.

    :param file_path: путь к JSON-файлу с транзакциями
    :return: список словарей с данными о финансовых транзакциях
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        logger.warning("Не удалось прочитать файл %s: %s", file_path, error)
        return []

    if not isinstance(data, list):
        logger.warning("JSON-файл %s содержит не список", file_path)
        return []

    return data


if __name__ == "__main__":
    print(load_transactions("data/operations.json"))