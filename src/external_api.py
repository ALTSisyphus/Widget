import os
from typing import Any, Dict

import requests  # type: ignore[import]

API_KEY_ENV = "EXCHANGE_RATES_API_KEY"
API_BASE = "https://api.apilayer.com/exchangerates_data/convert"
DEFAULT_TIMEOUT = 10


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Преобразует сумму транзакции в рубли и возвращает float.
    Возвращает 0.0 при ошибках (нечисловая сумма, отсутствие API-ключа или ошибка сети).
    """
    op = transaction.get("operationAmount") or {}
    raw_amount = op.get("amount", 0)

    try:
        amount = float(raw_amount)
    except (TypeError, ValueError):
        return 0.0

    cur_obj = op.get("currency")
    if isinstance(cur_obj, dict):
        currency = str(cur_obj.get("code", "")).upper()
    else:
        currency = str(cur_obj or "").upper()

    if not currency or currency == "RUB":
        return float(amount)

    if currency in ("USD", "EUR"):
        api_key = os.environ.get(API_KEY_ENV)
        if not api_key:
            return 0.0

        headers = {"apikey": api_key}
        params = {"from": currency, "to": "RUB", "amount": amount}

        try:
            resp = requests.get(API_BASE, headers=headers, params=params, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()

            if isinstance(data, dict):
                if "result" in data and data["result"] is not None:
                    return float(data["result"])
                rate = data.get("info", {}).get("rate")
                if rate is not None:
                    return float(rate) * float(amount)
            return 0.0
        except Exception:
            # Тесты ожидают 0.0 при Exception (например, mock.side_effect = Exception(...))
            return 0.0

    return float(amount)
