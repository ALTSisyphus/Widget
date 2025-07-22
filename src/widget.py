from .masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.
    :param data: Строка формата "Visa Platinum 7000792289606361" или "Счет 73654108430135874305"
    :return: Строка с замаскированным номером
    """
    # Определяем тип карты/счета
    parts = data.split()
    if not parts:
        return data

    # Извлекаем последнюю часть как номер
    number = parts[-1]

    if "счет" in data.lower():
        return f"{' '.join(parts[:-1])} {get_mask_account(number)}"
    elif number.isdigit() and len(number) == 16:
        return f"{' '.join(parts[:-1])} {get_mask_card_number(number)}"
    else:
        return data  # Возвращаем исходную строку для некорректных данных


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.
    :param date_str: Строка с датой в формате "2024-03-11T02:26:18.671407"
    :return: Строка с датой в формате "11.03.2024"
    """
    if not date_str:
        return ""

    try:
        # Разделяем дату и время
        date_part = date_str.split("T")[0]
        # Разбиваем на компоненты
        year, month, day = date_part.split("-")
        return f"{day}.{month}.{year}"
    except (IndexError, ValueError):
        return date_str  # Возвращаем исходную строку при ошибке
