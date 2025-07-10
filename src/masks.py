def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX.
    :param card_number: Номер карты (16 цифр)
    :return: Маскированная строка
    """
    # Безопасный способ разбиения без срезов с пробелами
    part1 = card_number[:4]
    part2 = card_number[4:6]
    part3 = card_number[-4:]
    return f"{part1} {part2}** **** {part3}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта в формате **XXXX.
    :param account_number: Номер счёта
    :return: Маскированная строка
    """
    return f"**{account_number[-4:]}"
