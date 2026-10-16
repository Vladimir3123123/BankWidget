## Чтение CSV и Excel (`src/csv_excel_reader.py`)

Модуль содержит функции для чтения финансовых операций из CSV- и Excel-файлов.

### `read_csv_file(file_path)`

Считывает операции из CSV-файла и возвращает список словарей.
При ошибке (файл не найден, пуст, битый CSV) возвращает `[]`.

```python
from src.csv_excel_reader import read_csv_file

transactions = read_csv_file("data/transactions.csv")
print(transactions)
```

### `read_excel_file(file_path)`

Считывает операции из Excel-файла (`.xlsx`) и возвращает список словарей.
При ошибке возвращает `[]`.

```python
from src.csv_excel_reader import read_excel_file

transactions = read_excel_file("data/transactions_excel.xlsx")
print(transactions)
```

### Зависимости

Для чтения Excel нужен `openpyxl`:

```bash
pip install pandas openpyxl
```
~~~~
### Логирование

В модуле настроен логер, который пишет в `logs/csv_excel_reader.log`.
Формат: `метка времени - имя модуля - уровень - сообщение`.