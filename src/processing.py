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
