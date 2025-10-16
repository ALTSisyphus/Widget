from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Параметризованные тесты для filter_by_currency
@pytest.mark.parametrize("currency, expected_count", [("USD", 3), ("RUB", 1), ("EUR", 0)])
def test_filter_by_currency(sample_transactions: List[Dict[str, Any]], currency: str, expected_count: int) -> None:
    filtered = filter_by_currency(sample_transactions, currency)
    count = sum(1 for _ in filtered)
    assert count == expected_count


# Тесты для transaction_descriptions
def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    descriptions = list(transaction_descriptions(sample_transactions))
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
    ]
    assert descriptions == expected


# Параметризованные тесты для card_number_generator
@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9998, 10000, ["0000 0000 0000 9998", "0000 0000 0000 9999", "0000 0000 0001 0000"]),
        (0, 0, ["0000 0000 0000 0000"]),
    ],
)
def test_card_number_generator(start: int, end: int, expected: List[str]) -> None:
    generator = card_number_generator(start, end)
    results = list(generator)
    assert results == expected
