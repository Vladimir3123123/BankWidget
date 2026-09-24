def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску.

    Формат маски: XXXX XX** **** XXXX
    """
    if not card_number or not card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    masked = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[12:16]
    return masked


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску.

    Формат маски: **XXXX
    """
    if not account_number or not account_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    if len(account_number) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")

    masked = "**" + account_number[-4:]
    return masked


if __name__ == "__main__":
    print(get_mask_card_number("7004347581766830"))
    print(get_mask_account("90123866543018304735"))