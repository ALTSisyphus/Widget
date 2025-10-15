"""Console entry point for the banking transactions helper."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from src.transactions import (
    filter_transactions_by_currency,
    filter_transactions_by_description,
    filter_transactions_by_status,
    format_transaction,
    load_transactions,
    sort_transactions_by_date,
)

MENU_OPTIONS: dict[str, tuple[str, Path]] = {
    "1": ("JSON", Path("data/operations.json")),
    "2": ("CSV", Path("data/operations.csv")),
    "3": ("XLSX", Path("data/operations.xlsx")),
}

AVAILABLE_STATUSES = ("EXECUTED", "CANCELED", "PENDING")
YES_ANSWERS = {"да", "д", "yes", "y"}
NO_ANSWERS = {"нет", "н", "no", "n"}
ASCENDING_ANSWERS = {"по возрастанию", "возрастание", "возрастающ", "asc", "ascending"}
DESCENDING_ANSWERS = {"по убыванию", "убывание", "убыв", "desc", "descending"}


def main(input_func: Callable[[str], str] | None = None) -> None:
    """Run an interactive session with the user."""

    if input_func is None:
        input_func = input

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = _prompt_menu_choice(input_func)
    file_label, file_path = MENU_OPTIONS[choice]
    print(f"Для обработки выбран {file_label}-файл.")

    transactions = _load_transactions_with_retry(file_path, file_label, input_func)

    status = _prompt_status(input_func)
    filtered = filter_transactions_by_status(transactions, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    if _ask_yes_no("Отсортировать операции по дате? Да/Нет", input_func):
        ascending = _prompt_sort_order(input_func)
        filtered = sort_transactions_by_date(filtered, ascending=ascending)

    if _ask_yes_no("Выводить только рублевые транзакции? Да/Нет", input_func):
        filtered = filter_transactions_by_currency(filtered, "RUB")

    if _ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет", input_func):
        search_term = _ask_question("Введите слово для поиска в описании:", input_func)
        filtered = filter_transactions_by_description(filtered, search_term)

    print("Распечатываю итоговый список транзакций...")
    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(filtered)}\n")
    for transaction in filtered:
        print(format_transaction(transaction))


def _prompt_menu_choice(input_func: Callable[[str], str]) -> str:
    """Запросить у пользователя пункт меню."""

    while True:
        choice = input_func("").strip()
        if choice in MENU_OPTIONS:
            return choice
        print("Пожалуйста, выберите пункт меню 1, 2 или 3.")


def _prompt_status(input_func: Callable[[str], str]) -> str:
    """Получить корректный статус операции от пользователя."""

    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        status = input_func("").strip().upper()
        if status in AVAILABLE_STATUSES:
            return status
        print(f'Статус операции "{status}" недоступен.')


def _ask_yes_no(question: str, input_func: Callable[[str], str]) -> bool:
    """Вернуть True/False в зависимости от ответа пользователя."""

    while True:
        print(question)
        answer = input_func("").strip().lower()
        if answer in YES_ANSWERS:
            return True
        if answer in NO_ANSWERS:
            return False
        print('Введите "Да" или "Нет".')


def _prompt_sort_order(input_func: Callable[[str], str]) -> bool:
    """Вернуть порядок сортировки по ответу пользователя."""

    while True:
        print("Отсортировать по возрастанию или по убыванию?")
        answer = input_func("").strip().lower()
        if any(token in answer for token in ASCENDING_ANSWERS):
            return True
        if any(token in answer for token in DESCENDING_ANSWERS):
            return False
        print('Введите "по возрастанию" или "по убыванию".')


def _ask_question(question: str, input_func: Callable[[str], str]) -> str:
    """Вывести вопрос и вернуть ответ пользователя."""

    print(question)
    return input_func("").strip()


def _load_transactions_with_retry(
    file_path: Path, label: str, input_func: Callable[[str], str]
) -> list[dict[str, object]]:
    """Загрузить транзакции, запрашивая путь до тех пор, пока это не удастся."""

    path = file_path
    while True:
        try:
            return load_transactions(path)
        except FileNotFoundError:
            print(f"Файл {path} не найден. Укажите путь к {label}-файлу:")
            path = Path(input_func("").strip())
        except (ValueError, ImportError) as error:
            print(error)
            print(f"Укажите корректный путь к {label}-файлу:")
            path = Path(input_func("").strip())


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
