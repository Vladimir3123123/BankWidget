import re
from collections import Counter
from typing import Any


def filter_by_state(data: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'.

    :param data: список словарей с данными о банковских операциях
    :param state: значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED')
    :return: новый список словарей, у которых state совпадает с переданным значением
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Сортирует список словарей по дате.

    :param data: список словарей с данными о банковских операциях
    :param reverse: порядок сортировки: True — по убыванию, False — по возрастанию
    :return: новый отсортированный список словарей
    """
    return sorted(data, key=lambda item: str(item.get("date", "")), reverse=reverse)


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Ищет транзакции, в описании которых встречается заданная строка.

    Поиск выполняется через регулярные выражения (без учёта регистра).

    :param data: список словарей с транзакциями
    :param search: строка для поиска в поле description
    :return: список словарей, у которых description содержит строку поиска
    """
    if not search:
        return list(data)

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [item for item in data if pattern.search(str(item.get("description", "")))]


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """Считает количество операций по каждой категории.

    Категории сопоставляются с полем description.

    :param data: список словарей с транзакциями
    :param categories: список категорий для подсчёта
    :return: словарь вида {категория: количество операций}
    """
    counter: Counter[str] = Counter()

    for item in data:
        description = str(item.get("description", ""))
        for category in categories:
            if category.lower() in description.lower():
                counter[category] += 1

    return {category: counter[category] for category in categories}


if __name__ == "__main__":
    sample = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    print(filter_by_state(sample))
    print(filter_by_state(sample, "CANCELED"))
    print(sort_by_date(sample))
    print(process_bank_search(sample, "перевод"))
    print(process_bank_operations(sample, ["Перевод организации"]))
