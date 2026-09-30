# BankWidget

Виджет банковских операций клиента: маскирование карт и счетов, обработка дат, фильтрация и сортировка операций, а также генераторы для работы с большими объёмами транзакций.

## Содержание

- [Установка](#установка)
- [Функционал](#функционал)
  - [Маскирование (`src/masks.py`)](#маскирование-srcmaskspy)
  - [Работа с виджетом (`src/widget.py`)](#работа-с-виджетом-srcwidgetpy)
  - [Обработка операций (`src/processing.py`)](#обработка-операций-srcprocessingpy)
  - [Генераторы (`src/generators.py`)](#генераторы-srcgeneratorspy)
- [Тестирование](#тестирование)

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Vladimir3123123/BankWidget.git
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
  ```python
  from src.masks import get_mask_card_number

  get_mask_card_number("7000792289606361")
  # "7000 79** **** 6361"
  ```

- `get_mask_account(account_number)` — маскирует номер счёта в формат `**XXXX`.
  ```python
  from src.masks import get_mask_account

  get_mask_account("73654108430135874305")
  # "**4305"
  ```

### Работа с виджетом (`src/widget.py`)

- `mask_account_card(info)` — принимает строку с типом и номером, возвращает замаскированную строку.
  ```python
  from src.widget import mask_account_card

  mask_account_card("Visa Platinum 7000792289606361")
  # "Visa Platinum 7000 79** **** 6361"

  mask_account_card("Счет 73654108430135874305")
  # "Счет **4305"
  ```

- `get_date(date_string)` — преобразует ISO-дату в формат `ДД.ММ.ГГГГ`.
  ```python
  from src.widget import get_date

  get_date("2024-03-11T02:26:18.671407")
  # "11.03.2024"
  ```

### Обработка операций (`src/processing.py`)

- `filter_by_state(data, state="EXECUTED")` — фильтрует операции по статусу.
  ```python
  from src.processing import filter_by_state

  operations = [
      {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
      {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
  ]

  filter_by_state(operations)
  # [{"id": 41428829, "state": "EXECUTED", ...}]

  filter_by_state(operations, "CANCELED")
  # [{"id": 594226727, "state": "CANCELED", ...}]
  ```

- `sort_by_date(data, reverse=True)` — сортирует операции по дате.
  ```python
  from src.processing import sort_by_date

  sort_by_date(operations)
  # по убыванию даты (сначала самые свежие)

  sort_by_date(operations, reverse=False)
  # по возрастанию
  ```

### Генераторы (`src/generators.py`)

Модуль содержит инструменты для эффективной работы с большими объёмами транзакций.

- `filter_by_currency(transactions, currency)` — возвращает итератор транзакций с заданной валютой.
  ```python
  from src.generators import filter_by_currency

  usd_transactions = filter_by_currency(transactions, "USD")
  for _ in range(2):
      print(next(usd_transactions))
  ```

- `transaction_descriptions(transactions)` — генератор, который по очереди возвращает описания операций.
  ```python
  from src.generators import transaction_descriptions

  descriptions = transaction_descriptions(transactions)
  for _ in range(5):
      print(next(descriptions))
  # Перевод организации
  # Перевод со счета на счет
  # ...
  ```

- `card_number_generator(start, stop)` — генератор номеров банковских карт в формате `XXXX XXXX XXXX XXXX`.
  ```python
  from src.generators import card_number_generator

  for card_number in card_number_generator(1, 5):
      print(card_number)
  # 0000 0000 0000 0001
  # 0000 0000 0000 0002
  # 0000 0000 0000 0003
  # 0000 0000 0000 0004
  # 0000 0000 0000 0005
  ```

## Тестирование

Проект покрыт тестами с использованием `pytest`.

### Установка зависимостей для тестов

```bash
pip install pytest pytest-cov
```

### Запуск тестов

```bash
pytest tests/ -v
```

### Проверка покрытия

```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

HTML-отчёт сохраняется в папку `htmlcov/`. Откройте `htmlcov/index.html` в браузере для просмотра детального отчёта.

### Структура тестов

- `tests/conftest.py` — общие фикстуры.
- `tests/test_masks.py` — тесты для `masks.py`.
- `tests/test_widget.py` — тесты для `widget.py`.
- `tests/test_processing.py` — тесты для `processing.py`.
- `tests/test_generators.py` — тесты для `generators.py`.

Все ключевые функции покрыты тестами, включая параметризованные проверки и граничные случаи. Покрытие — более 80%.

## Лицензия

Учебный проект.