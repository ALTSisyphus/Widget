from __future__ import annotations

import os
from decimal import Decimal
from typing import Any, Mapping

import requests
from dotenv import load_dotenv

API_BASE = "https://api.apilayer.com/exchangerates_data"


def amount_in_rub(transaction: Mapping[str, Any]) -> float:
    """
    Возвращает сумму транзакции (operationAmount.amount) в рублях.
    - Если валюта RUB — просто возвращает сумму.
    - Если USD или EUR — обращается к внешнему API и конвертирует в RUB.
    - Для остальных валют возвращает сумму без конвертации.

    Ожидаемый формат транзакции (как в operations.json):
    {
      "operationAmount": {
        "amount": "8221.37",
        "currency": {"name": "USD", "code": "USD"}
      },
      ...
    }

    :param transaction: Словарь с данными транзакции.
    :return: Сумма в рублях (float).
    :raises RuntimeError: если не задан API_KEY или ответ API некорректен/недоступен.
    """
    op = transaction.get("operationAmount") if isinstance(transaction, Mapping) else None
    if not isinstance(op, Mapping):
        return 0.0

    amount_raw = op.get("amount")
    currency = op.get("currency") or {}
    code = str(currency.get("code") or "").upper()

    # Парсинг суммы
    try:
        amount_dec = Decimal(str(amount_raw).replace(",", "."))
    except Exception:
        return 0.0

    # Быстрый путь: рубли
    if code in ("", "RUB"):
        return float(amount_dec)

    # Конвертация только для USD/EUR по условию задачи
    if code not in ("USD", "EUR"):
        return float(amount_dec)

    # Ключ из .env
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY is not set. Укажи ключ в .env или переменных окружения.")

    # Используем endpoint /convert
    url = f"{API_BASE}/convert"
    params = {"to": "RUB", "from": code, "amount": str(amount_dec)}
    headers = {"apikey": api_key}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        payload = resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Currency API error: {e}") from e

    # Нормальный ответ Apilayer содержит поле 'result'
    result = None
    if isinstance(payload, dict):
        if "result" in payload:
            result = payload["result"]
        elif "info" in payload and isinstance(payload["info"], dict) and "rate" in payload["info"]:
            # fallback: если вернулся rate, сами перемножим
            rate = Decimal(str(payload["info"]["rate"]))
            result = float(rate * amount_dec)

    if result is None:
        raise RuntimeError("Unexpected response from currency API")

    return float(result)
