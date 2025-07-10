from .masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.
    :param data: Строка формата "Visa Platinum 7000792289606361" или "Счет 73654108430135874305"
    :return: Строка с замаскированным номером
    """
    # Определяем тип карты/счета
    if "счет" in data.lower():
        # Ищем начало номера счета
        parts = data.split()
        account_number = parts[-1]
        return f"{' '.join(parts[:-1])} {get_mask_account(account_number)}"
    else:
        # Для карт
        parts = data.split()
        card_number = parts[-1]
        return f"{' '.join(parts[:-1])} {get_mask_card_number(card_number)}"


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.
    :param date_str: Строка с датой в формате "2024-03-11T02:26:18.671407"
    :return: Строка с датой в формате "11.03.2024"
    """
    # Разделяем дату и время
    date_part = date_str.split("T")[0]
    # Разбиваем на компоненты
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"
