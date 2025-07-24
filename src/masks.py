def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX.
    :param card_number: Номер карты (16 цифр)
    :return: Маскированная строка
    """
    if len(card_number) < 6:
        return card_number  # Возвращаем как есть для коротких номеров

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта в формате **XXXX.
    :param account_number: Номер счёта
    :return: Маскированная строка
    """
    if not account_number:
        return ""

    if len(account_number) < 4:
        return f"**{account_number}"

    return f"**{account_number[-4:]}"
