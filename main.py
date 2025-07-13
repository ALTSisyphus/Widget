from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card

# Тест для карты
print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361

# Тест для счёта
print(get_mask_account("73654108430135874305"))  # **4305

# Тестирование функции маскировки
test_cases = [
    "Visa Platinum 7000792289606361",
    "Maestro 1596837868705199",
    "Счет 64686473678894779589",
    "MasterCard 7158300734726758",
    "Счет 35383033474447895560",
    "Visa Classic 6831982476737658",
    "Visa Platinum 8990922113665229",
    "Visa Gold 5999414228426353",
    "Счет 73654108430135874305",
]

for case in test_cases:
    print(mask_account_card(case))

# Тестирование функции даты
print("\nТестирование даты:")
print(get_date("2024-03-11T02:26:18.671407"))  # Должно вернуть "11.03.2024"

# Тестовые данные
operations = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

# Фильтрация по статусу
print("Фильтрация по EXECUTED:")
for op in filter_by_state(operations):
    print(op)

print("\nФильтрация по CANCELED:")
for op in filter_by_state(operations, "CANCELED"):
    print(op)

# Сортировка по дате
print("\nСортировка по убыванию (новые первые):")
for op in sort_by_date(operations):
    print(op)

print("\nСортировка по возрастанию (старые первые):")
for op in sort_by_date(operations, reverse=False):
    print(op)
