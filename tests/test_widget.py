from src.widget import get_date, mask_account_card


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
