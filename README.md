# Widget with logging — CSV/XLSX transactions support

Добавлена поддержка чтения финансовых транзакций из CSV и Excel (XLSX) файлов с помощью `pandas`.

## Новая функциональность

- `src/io_transactions.py`
  - `read_transactions_csv(path: str | Path, *, encoding: str | None = None, sep: str = ",") -> list[dict]`
  - `read_transactions_excel(path: str | Path, *, sheet_name: int | str | None = 0) -> list[dict]`

Обе функции возвращают список словарей c транзакциями. Ключи — названия колонок.

## Как использовать

```python
from src.io_transactions import read_transactions_csv, read_transactions_excel

rows_csv = read_transactions_csv("data/transactions.csv")
rows_xlsx = read_transactions_excel("data/transactions.xlsx")
```

## Тесты

Добавлены тесты `tests/test_io_transactions.py` (используются `Mock` и `patch`).

Запуск тестов:

```bash
pytest -q
```
