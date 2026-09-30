from collections.abc import Iterator
from typing import Any


def filter_by_currency(
    transactions: list[dict[str, Any]], currency: str
) -> Iterator[dict[str, Any]]:
    """Возвращает итератор транзакций с заданной валютой.

    :param transactions: список словарей с данными о транзакциях
    :param currency: код валюты (например, "USD", "RUB")
    :return: итератор словарей, у которых код валюты совпадает с переданным
    """
    for transaction in transactions:
        code = transaction.get("operationAmount", {}).get("currency", {}).get("code")
        if code == currency:
            yield transaction


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Iterator[str]:
    """Генерирует описания транзакций по очереди.

    :param transactions: список словарей с данными о транзакциях
    :return: генератор строк с описанием каждой операции
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.

    :param start: начальное значение диапазона (включительно)
    :param stop: конечное значение диапазона (включительно)
    :return: генератор строк с номерами карт
    """
    for number in range(start, stop + 1):
        card_str = str(number).zfill(16)
        formatted = (
            f"{card_str[0:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        )
        yield formatted


if __name__ == "__main__":
    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
        },
    ]

    usd = filter_by_currency(sample_transactions, "USD")
    print(next(usd))
    print(next(usd))

    for desc in transaction_descriptions(sample_transactions):
        print(desc)

    for card in card_number_generator(1, 5):
        print(card)