from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """
    Фильтрует транзакции по валюте операции.
    :param transactions: Список транзакций
    :param currency: Код валюты (например, "USD")
    :return: Итератор, возвращающий транзакции с указанной валютой
    """
    for transaction in transactions:
        op_amount = transaction.get("operationAmount", {})
        curr = op_amount.get("currency", {})
        if curr.get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """
    Генерирует описания транзакций.
    :param transactions: Список транзакций
    :return: Итератор, возвращающий описания транзакций
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.
    :param start: Начальный номер карты
    :param end: Конечный номер карты
    :return: Итератор, возвращающий номера карт в формате "XXXX XXXX XXXX XXXX"
    """
    for num in range(start, end + 1):
        # Форматируем номер с ведущими нулями
        card_num = str(num).zfill(16)
        # Разбиваем на группы по 4 цифры (убираем пробел перед :)
        formatted = " ".join([card_num[i : i + 4] for i in range(0, 16, 4)])
        yield formatted
