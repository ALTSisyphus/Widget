from src.masks import get_mask_account, get_mask_card_number

# Тест для карты
print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361

# Тест для счёта
print(get_mask_account("73654108430135874305"))  # **4305
