from src.csv_excel_reader import read_csv_file, read_excel_file
from src.external_api import convert_to_rub
from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card

VALID_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def ask_yes_no(question: str) -> bool:
    """Спрашивает у пользователя Да/Нет и возвращает True для «да».

    :param question: текст вопроса
    :return: True, если пользователь ответил «да»
    """
    while True:
        answer = input(question).strip().lower()
        if answer in ("да", "yes", "y", "д"):
            return True
        if answer in ("нет", "no", "n", "н"):
            return False
        print("Пожалуйста, ответьте «да» или «нет».")


def choose_source() -> list[dict]:
    """Предлагает пользователю выбрать источник данных.

    :return: список транзакций из выбранного файла
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input().strip()
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            return load_transactions("data/operations.json")
        if choice == "2":
            print("Для обработки выбран CSV-файл.")
            return read_csv_file("data/transactions.csv")
        if choice == "3":
            print("Для обработки выбран XLSX-файл.")
            return read_excel_file("data/transactions_excel.xlsx")
        print("Некорректный выбор. Введите 1, 2 или 3.")


def ask_status() -> str:
    """Спрашивает у пользователя статус операций, пока не получит валидный.

    :return: валидный статус в верхнем регистре
    """
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            f"Доступные для фильтровки статусы: {', '.join(VALID_STATUSES)}"
        )
        status = input().strip().upper()
        if status in VALID_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        print(f'Статус операции "{status}" недоступен.')


def print_transactions(transactions: list[dict]) -> None:
    """Выводит список транзакций в человекочитаемом виде.

    :param transactions: список словарей с транзакциями
    """
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for item in transactions:
        date = get_date(item.get("date", ""))
        description = item.get("description", "")
        print(f"{date} {description}")

        from_acc = item.get("from")
        to_acc = item.get("to")
        if from_acc and to_acc:
            print(f"{mask_account_card(from_acc)} -> {mask_account_card(to_acc)}")
        elif to_acc:
            print(mask_account_card(to_acc))

        amount = item.get("operationAmount", {}).get("amount")
        currency = item.get("operationAmount", {}).get("currency", {}).get("name", "")
        print(f"Сумма: {amount} {currency}")
        print()


def main() -> None:
    """Основная логика программы: интерактивное меню обработки транзакций."""
    transactions = choose_source()

    status = ask_status()
    transactions = filter_by_state(transactions, status)

    if ask_yes_no("Отсортировать операции по дате? Да/Нет"):
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        reverse = order.startswith("убыв")
        transactions = sort_by_date(transactions, reverse=reverse)

    if ask_yes_no("Выводить только рублевые транзакции? Да/Нет"):
        transactions = [
            item for item in transactions if item.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"):
        search = input("Введите слово для поиска: ").strip()
        transactions = process_bank_search(transactions, search)

    print("Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print_transactions(transactions)


if __name__ == "__main__":
    main()
