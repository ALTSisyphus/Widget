from typing import Dict, Iterator, List


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    """
    Фильтрует транзакции по коду валюты.

    :param transactions: Список транзакций (каждая транзакция — dict)
    :param currency: Код валюты (например, 'USD' или 'RUB')
    :return: Итератор, возвращающий транзакции с указанной валютой
    """
    target = (currency or "").upper()
    for transaction in transactions:
        op_amount = transaction.get("operationAmount", {}) or {}
        curr = op_amount.get("currency", {}) or {}
        code = ""
        if isinstance(curr, dict):
            code = str(curr.get("code", "")).upper()
        else:
            code = str(curr).upper()
        if code == target:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Возвращает описания транзакций (поле 'description').

    :param transactions: Список транзакций
    :return: Итератор строк с описаниями
    """
    for tr in transactions:
        yield str(tr.get("description", ""))


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.

    Номера форматируются группами по 4 цифры: "XXXX XXXX XXXX XXXX".
    """
    for num in range(start, end + 1):
        card_num = str(num).zfill(16)
        # здесь важно: без пробелов вокруг ':' чтобы не было E203
        formatted = " ".join([card_num[i : i + 4] for i in range(0, 16, 4)])
        yield formatted
