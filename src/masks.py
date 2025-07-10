def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX.
    :param card_number: Номер карты (16 цифр)
    :return: Маскированная строка
    """
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта в формате **XXXX.
    :param account_number: Номер счёта
    :return: Маскированная строка
    """
    return f"**{account_number[-4:]}"