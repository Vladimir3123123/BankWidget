## Поиск и подсчёт операций (`src/processing.py`)

### `process_bank_search(data, search)`

Ищет транзакции, в описании которых встречается заданная строка. Использует библиотеку `re` (без учёта регистра).

```python
from src.processing import process_bank_search

result = process_bank_search(transactions, "Перевод")
```

### `process_bank_operations(data, categories)`

Считает количество операций по каждой категории из поля `description`.
Использует `Counter` из `collections`.

```python
from src.processing import process_bank_operations

result = process_bank_operations(
    transactions, ["Перевод организации", "Открытие вклада"]
)
# {"Перевод организации": 5, "Открытие вклада": 2}
```

## Интерактивное меню (`src/main.py`)

Модуль предоставляет пользовательский интерфейс для работы с транзакциями.

Запуск:

```bash
python -m src.main
```

Пользователь последовательно выбирает:
1. Источник данных (JSON, CSV, XLSX).
2. Статус операций (EXECUTED, CANCELED, PENDING).
3. Нужна ли сортировка по дате.
4. Оставить только рублёвые транзакции.
5. Фильтр по слову в описании.

После этого программа выводит итоговый список операций.