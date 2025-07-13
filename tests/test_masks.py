import pytest

from src.masks import get_mask_account, get_mask_card_number


# Фикстура для тестовых данных карт
@pytest.fixture
def card_numbers() -> list[tuple[str, str]]:
    return [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1596837868705199", "1596 83** **** 5199"),
        ("", "** **"),  # Обработка пустой строки
        ("1234", "1234 ** ** **** "),  # Обработка короткого номера
    ]


# Фикстура для тестовых данных счетов
@pytest.fixture
def account_numbers() -> list[tuple[str, str]]:
    return [
        ("73654108430135874305", "**4305"),
        ("64686473678894779589", "**9589"),
        ("", "**"),  # Обработка пустой строки
        ("123", "**123"),  # Обработка короткого номера
    ]


# Параметризованные тесты для карт
def test_get_mask_card_number(card_numbers: list[tuple[str, str]]) -> None:
    for input_card, expected in card_numbers:
        result = get_mask_card_number(input_card)
        assert result == expected


# Параметризованные тесты для счетов
def test_get_mask_account(account_numbers: list[tuple[str, str]]) -> None:
    for input_account, expected in account_numbers:
        result = get_mask_account(input_account)
        assert result == expected
