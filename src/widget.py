from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_info: str) -> str:
    """Функция принимает строку с типом и номером карты или счета
    и возвращает строку с замаскированным номером.

    Примеры:
        Visa Platinum 7000792289606361 -> Visa Platinum 7000 79** **** 6361
        Счет 73654108430135874305 -> Счет **4305
    """
    if not account_card_info or not account_card_info.strip():
        raise ValueError("Входная строка не может быть пустой")

    parts = account_card_info.strip().split()

    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип и номер")

    number = parts[-1]
    name = " ".join(parts[:-1])

    if not number.isdigit():
        raise ValueError("Номер должен содержать только цифры")

    if name.lower().startswith("счет"):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """Функция принимает строку с датой в ISO-формате и возвращает
    строку в формате ДД.ММ.ГГГГ.

    Пример:
        2024-03-11T02:26:18.671407 -> 11.03.2024
    """
    if not date_string:
        raise ValueError("Строка с датой не может быть пустой")

    date_obj = datetime.fromisoformat(date_string)
    return date_obj.strftime("%d.%m.%Y")


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(mask_account_card("MasterCard 7158300734726758"))
    print(get_date("2024-03-11T02:26:18.671407"))