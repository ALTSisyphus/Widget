from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Literal, TypedDict


class Money(TypedDict, total=False):
    """Денежная часть операции."""
    amount: float
    currency: str


class Transaction(TypedDict, total=False):
    """Транзакция в унифицированном формате."""
    id: str
    date: str
    description: str
    status: Literal["EXECUTED", "CANCELED", "PENDING"]
    from_: str | None
    to: str | None
    operationAmount: Money


SUPPORTED_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}



def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Вернуть операции, где в description найдено совпадение с шаблоном `search`.
    Поиск регистронезависимый. Используется модуль `re`.

    :param data: список словарей-операций
    :param search: строка / регулярное выражение
    :return: список словарей с подходящими операциями
    """
    pattern = re.compile(search, re.IGNORECASE)
    return [op for op in data if pattern.search(str(op.get("description", "")))]



def process_bank_operations(data: list[dict], categories: Iterable[str]) -> dict[str, int]:
    """
    Подсчитать количество операций по списку категорий (ищем подстроку в `description`).
    Возвращает словарь {категория: число операций}.

    :param data: список словарей-операций
    :param categories: список названий категорий
    """
    cnt: Counter[str] = Counter()
    for cat in categories:
        needle = cat.lower()
        for op in data:
            if needle in str(op.get("description", "")).lower():
                cnt[cat] += 1
    return dict(cnt)



def load_transactions(path: str | Path) -> list[Transaction]:
    """
    Загрузить транзакции из JSON/CSV/XLSX и привести к типу Transaction.
    Для XLSX требуется pandas+openpyxl (опционально).
    """
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".json":
        with p.open(encoding="utf-8") as f:
            raw = json.load(f)
        return _normalize_list(raw)

    if ext == ".csv":
        out: list[Transaction] = []
        with p.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                out.append(_row_to_tx(row))
        return out

    if ext == ".xlsx":
        try:
            import pandas as pd  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError("Для чтения .xlsx установите pandas и openpyxl") from e
        df = pd.read_excel(p)  # type: ignore
        return [_row_to_tx(dict(row)) for _, row in df.iterrows()]

    raise ValueError(f"Неподдерживаемый формат файла: {ext}")


def _row_to_tx(row: dict[str, Any]) -> Transaction:
    """Привести произвольную запись к типу Transaction."""
    amount = row.get("amount") or row.get("operationAmount.amount")
    currency = row.get("currency") or row.get("operationAmount.currency")

    op_amount: Money = {}
    if amount is not None:
        try:
            op_amount["amount"] = float(amount)
        except Exception:
            pass
    if currency:
        op_amount["currency"] = str(currency)

    return Transaction(
        id=str(row.get("id", "")),
        date=str(row.get("date", "")),
        description=str(row.get("description", "")),
        status=str(row.get("status", "")).upper() or "PENDING",
        from_=row.get("from") or row.get("from_") or "",
        to=row.get("to") or "",
        operationAmount=op_amount,
    )


def _normalize_list(data: Any) -> list[Transaction]:
    out: list[Transaction] = []
    if isinstance(data, list):
        for row in data:
            if isinstance(row, dict):
                out.append(_row_to_tx(row))
    return out


def filter_by_status(data: list[Transaction], status: str) -> list[Transaction]:
    """Оставить операции только с выбранным статусом (ввод пользователя регистронезависим)."""
    target = status.upper()
    return [op for op in data if str(op.get("status", "")).upper() == target]


def sort_by_date(data: list[Transaction], ascending: bool) -> list[Transaction]:
    """Отсортировать по дате; поддержка ISO и простых форматов."""
    def _parse(s: str) -> datetime:
        s = s.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(s)
        except Exception:
            for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
                try:
                    return datetime.strptime(s, fmt)
                except Exception:
                    continue
            return datetime.min
    return sorted(data, key=lambda x: _parse(x.get("date", "")), reverse=not ascending)


def filter_rub_only(data: list[Transaction]) -> list[Transaction]:
    """Оставить только операции в рублях (по коду валюты)."""
    rub = {"RUB", "RUR", "РУБ", "РУБ."}
    out: list[Transaction] = []
    for op in data:
        cur = (op.get("operationAmount", {}) or {}).get("currency", "")
        if str(cur).upper() in rub:
            out.append(op)
    return out


def format_date_ru(s: str) -> str:
    """Дата в формате DD.MM.YYYY (если парсинг возможен)."""
    s = s.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s).strftime("%d.%m.%Y")
    except Exception:
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(s, fmt).strftime("%d.%m.%Y")
            except Exception:
                continue
        return s


def _mask_account(s: str | None) -> str:
    """
    Маскировка реквизитов:
    - 'Счет 1234567890' -> 'Счет **7890'
    - для карт оставить последние 4 цифры, остальные — '*'
    """
    if not s:
        return "-"
    # Счёт
    m = re.search(r"(Счет|Счёт)\s+(\d{4,})", s, flags=re.IGNORECASE)
    if m:
        return f"{m.group(1)} **{m.group(2)[-4:]}"
    # Карта — оставим последние 4
    digits = re.sub(r"\D", "", s)
    return s if len(digits) < 4 else re.sub(r"\d(?=\d{4}$)", "*", s)


def pretty_print(op: Transaction) -> str:
    """Человекочитаемый вывод операции (как в примере из задания)."""
    date = format_date_ru(op.get("date", ""))
    desc = op.get("description", "")
    frm = _mask_account(op.get("from_"))
    to = _mask_account(op.get("to"))
    amt = op.get("operationAmount", {}).get("amount", "")
    cur = op.get("operationAmount", {}).get("currency", "")
    lines = [f"{date} {desc}"]
    if frm != "-" and to != "-":
        lines.append(f"{frm} -> {to}")
    elif frm != "-":
        lines.append(frm)
    elif to != "-":
        lines.append(to)
    if amt != "" or cur != "":
        lines.append(f"Сумма: {amt} {cur}")
    return "\n".join(lines)
