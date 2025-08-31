"""Вспомогательные функции для работы с внешним API конвертации валют."""

import os
from typing import Any, Dict

import requests

API_KEY_ENV = "EXCHANGE_RATES_API_KEY"  # имя переменной окружения с API-ключом
API_BASE = "https://api.apilayer.com/exchangerates_data/convert"  # базовый URL для вызова конверта


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Преобразует сумму транзакции в рубли и возвращает ее как плавающую.

        Если валюта уже указана в рублях или не может быть проанализирована, возвращает числовую сумму
        как плавающую (или 0.0 в случае неустранимой ошибки). Для долларов США и евро функция
    вызывает API-интерфейс конвертации, используя ключ API, хранящийся в переменной среды
        EXCHANGE_RATES_API_KEY.

        Аргументы:
            транзакция: Словарь транзакций, содержащий как минимум ключи:
                operationAmount -> сумма (str или число)
                Сумма операции -> валюта -> код (например, "USD", "EUR","RUB")

        Возвращается:
            Сумма в рублях с плавающей запятой.
    """
    # Извлекаем сумму и код валюты из структуры транзакции
    try:
        op = transaction.get("operationAmount", {})
        amount_raw = op.get("amount")
        currency = op.get("currency", {}).get("code", "RUB")
        amount = float(amount_raw)
    except Exception:
        # Если не удалось извлечь или привести amount к числу — возвращаем 0.0
        return 0.0

    # Если валюта уже рубли — возвращаем сумму как float
    if currency.upper() == "RUB" or currency == "руб.":
        return float(amount)

    # Для USD или EUR выполняем вызов внешнего API для получения конвертированной суммы
    if currency.upper() in ("USD", "EUR"):
        # Берём ключ API из окружения и формируем заголовки/параметры запроса
        api_key = os.getenv(API_KEY_ENV, "")
        headers = {"apikey": api_key} if api_key else {}
        params = {"from": currency.upper(), "to": "RUB", "amount": str(amount)}
        try:
            # Выполняем HTTP GET к endpoint'у конвертации
            resp = requests.get(API_BASE, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            # Обычно endpoint возвращает поле 'result' — сконвертированную сумму
            result = data.get("result")
            if result is None:
                # Если 'result' отсутствует, пытаемся использовать поле 'info.rate' как курс
                rate = data.get("info", {}).get("rate")
                if rate is None:
                    # Не удалось получить курс — возвращаем 0.0
                    return 0.0
                # Возвращаем product rate * amount
                return float(rate) * float(amount)
            # Приводим результат к float и возвращаем
            return float(result)
        except Exception:
            # В случае любых ошибок сетевого взаимодействия или парсинга — безопасно вернуть 0.0
            return 0.0

    # For other currencies - return amount as is (could be extended)
    return float(amount)
