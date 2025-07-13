import pytest

from src.widget import get_date, mask_account_card


# Фикстура для тестовых данных карт и счетов
@pytest.fixture
def account_card_data() -> list[tuple[str, str]]:
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 123", "Счет **123"),  # Короткий номер счета
        ("Карта 1234567890123456", "Карта 1234 56** **** 3456"),  # Нестандартный тип
        ("Invalid Input", "Invalid Input"),  # Некорректные данные
    ]


# Фикстура для тестовых дат
@pytest.fixture
def date_data() -> list[tuple[str, str]]:
    return [
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
        ("", ""),  # Пустая строка
        ("Invalid Date", "Invalid Date"),  # Некорректные данные
    ]


# Параметризованные тесты для маскировки
def test_mask_account_card(account_card_data: list[tuple[str, str]]) -> None:
    for input_data, expected in account_card_data:
        result = mask_account_card(input_data)
        assert result == expected


# Параметризованные тесты для дат
def test_get_date(date_data: list[tuple[str, str]]) -> None:
    for input_date, expected in date_data:
        result = get_date(input_date)
        assert result == expected
