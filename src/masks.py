import logging
import os

# Создаём папку logs, если её нет
os.makedirs("logs", exist_ok=True)

# Логер для модуля masks
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Обработчик: пишем в файл logs/masks.log, режим "w" — перезапись при запуске
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")

# Формат: дата/время — имя модуля — уровень — сообщение
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)

# Добавляем handler к логеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску.

    Формат маски: XXXX XX** **** XXXX
    """
    logger.debug("Вызвана get_mask_card_number с аргументом: %s", card_number)

    if not card_number or not card_number.isdigit():
        logger.error("Некорректный ввод: номер карты должен содержать только цифры")
        raise ValueError("Номер карты должен содержать только цифры")

    if len(card_number) != 16:
        logger.error("Некорректная длина номера карты: %d", len(card_number))
        raise ValueError("Номер карты должен содержать 16 цифр")

    masked = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[12:16]
    logger.info("Успешно замаскирован номер карты: %s", masked)
    return masked


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску.

    Формат маски: **XXXX
    """
    logger.debug("Вызвана get_mask_account с аргументом: %s", account_number)

    if not account_number or not account_number.isdigit():
        logger.error("Некорректный ввод: номер счета должен содержать только цифры")
        raise ValueError("Номер счета должен содержать только цифры")

    if len(account_number) != 20:
        logger.error("Некорректная длина номера счета: %d", len(account_number))
        raise ValueError("Номер счета должен содержать 20 цифр")

    masked = "**" + account_number[-4:]
    logger.info("Успешно замаскирован номер счета: %s", masked)
    return masked


if __name__ == "__main__":
    print(get_mask_card_number("7004347581766830"))
    print(get_mask_account("90123866543018304735"))