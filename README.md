# BankWidget

Виджет банковских операций клиента: маскирование карт и счетов, обработка дат, фильтрация и сортировка операций.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ВАШ_ЛОГИН/BankWidget.git
   cd BankWidget
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate # Linux/macOS
   ```

3. Установите зависимости:
   ```bash
   pip install poetry
   poetry install
   ```

## Функционал

### Маскирование (`src/masks.py`)

- `get_mask_card_number(card_number)` — маскирует номер карты в формат `XXXX XX** **** XXXX`.
- `get_mask_account(account_number)` — маскирует номер счёта в формат `**XXXX`.

### Работа с виджетом (`src/widget.py`)

- `mask_account_card(info)` — принимает строку с типом и номером, возвращает замаскированную строку.
- `get_date(date_string)` — преобразует ISO-дату в формат `ДД.ММ.ГГГГ`.

### Обработка операций (`src/processing.py`)

- `filter_by_state(data, state="EXECUTED")` — фильтрует операции по статусу.
- `sort_by_date(data, reverse=True)` — сортирует операции по дате.

## Примеры использования

```python
from src.processing import filter_by_state, sort_by_date

operations = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
]

print(filter_by_state(operations))
print(filter_by_state(operations, "CANCELED"))
print(sort_by_date(operations))
```