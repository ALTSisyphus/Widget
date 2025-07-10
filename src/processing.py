def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует операции по статусу выполнения.
    :param operations: Список операций (словарей)
    :param state: Статус операции (по умолчанию 'EXECUTED')
    :return: Отфильтрованный список операций
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует операции по дате.
    :param operations: Список операций (словарей)
    :param reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)
    :return: Отсортированный список операций
    """
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)