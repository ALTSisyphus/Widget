from __future__ import annotations

from src.processing import (
    SUPPORTED_STATUSES,
    filter_by_status,
    filter_rub_only,
    load_transactions,
    pretty_print,
    process_bank_search,
    sort_by_date,
)


def _ask(prompt: str) -> str:
    """Безопасный input с обрезкой пробелов."""
    return input(prompt).strip()


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = _ask("Ваш выбор: ")
    ext = {"1": ".json", "2": ".csv", "3": ".xlsx"}.get(choice)
    if not ext:
        print("Некорректный выбор. Завершение работы.")
        return

    print(f"Для обработки выбран {ext.upper()}-файл.")
    path = _ask("Укажите путь к файлу с транзакциями: ")

    try:
        data = load_transactions(path)
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return

    # Фильтрация по статусу
    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
    while True:
        status = _ask("Статус: ").upper()
        if status in SUPPORTED_STATUSES:
            break
        print(f'Статус операции "{status}" недоступен.')
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    data = filter_by_status(data, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    # Сортировка по дате
    if _ask("Отсортировать операции по дате? Да/Нет: ").lower() in {"да", "y", "yes"}:
        order = _ask("Отсортировать по возрастанию или по убыванию? ").lower()
        ascending = ("возрастан" in order) or ("asc" in order)
        data = sort_by_date(data, ascending=ascending)

    # Только рублевые
    if _ask("Выводить только рублевые транзакции? Да/Нет: ").lower() in {"да", "y", "yes"}:
        data = filter_rub_only(data)

    # Поиск по слову/фразе (regexp) в описании
    if _ask("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").lower() in {"да", "y", "yes"}:
        needle = _ask("Введите слово/фразу (можно использовать регулярное выражение): ")
        data = process_bank_search(data, needle)

    print("\nРаспечатываю итоговый список транзакций...\n")
    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(data)}\n")
    for op in data:
        print(pretty_print(op))
        print()  # пустая строка между операциями


if __name__ == "__main__":
    main()
