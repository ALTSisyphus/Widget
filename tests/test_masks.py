from src.masks import get_mask_account, get_mask_card_number


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
