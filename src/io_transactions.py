"""Модуль для чтения финансовых транзакций из CSV и Excel (XLSX) файлов.

В модуле реализованы две функции:

- :func:`read_transactions_csv` — читает транзакции из CSV-файла.
- :func:`read_transactions_excel` — читает транзакции из Excel-файла.

Обе функции возвращают список словарей, где каждая строка файла
соответствует одной транзакции (ключи словаря — названия колонок).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, cast

import pandas as pd

# Определяем псевдоним для типа транзакции
Transaction = Dict[str, Any]


def _normalize_path(path: str | Path) -> Path:
    """Вернуть нормализованный путь к файлу.

    Принимает строку или объект :class:`Path`.
    Раскрывает тильду ``~`` в домашний каталог пользователя.

    Параметры
    ----------
    path : str | Path
        Путь к файлу.

    Возвращает
    ----------
    Path
        Нормализованный объект пути.

    Исключения
    ----------
    FileNotFoundError
        Если файл не существует.
    """
    p = Path(path).expanduser()
    if not p.exists():
        raise FileNotFoundError(f"Файл не найден: {p}")
    return p


def _df_to_transactions(df: pd.DataFrame) -> List[Transaction]:
    """Преобразовать DataFrame в список словарей с транзакциями.

    Каждая строка датафрейма превращается в словарь.
    Ключи совпадают с названиями колонок.

    Параметры
    ----------
    df : pd.DataFrame
        Таблица с транзакциями.

    Возвращает
    ----------
    list[dict]
        Список словарей (транзакций).
    """
    return cast(List[Transaction], df.to_dict(orient="records"))


def read_transactions_csv(
    path: str | Path, *, encoding: str | None = None, sep: str = ","
) -> List[Transaction]:
    """Прочитать финансовые транзакции из CSV-файла.

    Параметры
    ----------
    path : str | Path
        Путь к CSV-файлу.
    encoding : str | None, по умолчанию None
        Кодировка файла. Если не указана — :mod:`pandas` попытается определить её сам.
    sep : str, по умолчанию ","
        Разделитель полей в CSV.

    Возвращает
    ----------
    list[dict]
        Список словарей с транзакциями.

    Исключения
    ----------
    FileNotFoundError
        Если файл не существует.
    pandas.errors.EmptyDataError
        Если файл пустой.
    pandas.errors.ParserError
        Если не удалось распарсить CSV.
    """
    csv_path = _normalize_path(path)
    df = pd.read_csv(csv_path, encoding=encoding, sep=sep)  # type: ignore[arg-type]
    return _df_to_transactions(df)


def read_transactions_excel(
    path: str | Path, *, sheet_name: int | str | None = 0
) -> List[Transaction]:
    """Прочитать финансовые транзакции из Excel-файла (XLSX).

    Параметры
    ----------
    path : str | Path
        Путь к XLSX-файлу.
    sheet_name : int | str | None, по умолчанию 0
        Лист Excel для чтения: индекс (0, 1, 2...) или имя.

    Возвращает
    ----------
    list[dict]
        Список словарей с транзакциями.

    Исключения
    ----------
    FileNotFoundError
        Если файл не существует.
    ValueError
        Если указанный лист не найден.
    """
    xlsx_path = _normalize_path(path)
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name)  # type: ignore[arg-type]
    return _df_to_transactions(df)
