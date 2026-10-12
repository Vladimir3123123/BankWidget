import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/convert"
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")


def convert_to_rub(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли.

    Если транзакция уже в рублях — возвращает сумму как есть.
    Если в USD или EUR — обращается к внешнему API за курсом
    и возвращает сконвертированную сумму.

    :param transaction: словарь с данными о транзакции
    :return: сумма транзакции в рублях (float)
    """
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0))
    currency = operation_amount.get("currency", {}).get("code", "RUB")

    if currency == "RUB":
        return amount

    if currency not in ("USD", "EUR"):
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    if not API_KEY:
        raise ValueError("Не задан EXCHANGE_RATES_API_KEY в .env")

    response = requests.get(
        API_URL,
        headers={"apikey": API_KEY},
        params={"from": currency, "to": "RUB", "amount": amount},
        timeout=10,
    )
    response.raise_for_status()
    result = response.json()

    return float(result["result"])


if __name__ == "__main__":
    sample = {
        "operationAmount": {
            "amount": "8221.37",
            "currency": {"name": "USD", "code": "USD"},
        }
    }
    print(convert_to_rub(sample))