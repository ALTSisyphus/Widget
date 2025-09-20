import logging
from pathlib import Path

# Настройка ведения журнала для модуля masks
_project_root = Path(__file__).resolve().parents[1]
_logs_dir = _project_root / "logs"
_logs_dir.mkdir(parents=True, exist_ok=True)
_logger = logging.getLogger("masks")
if not _logger.handlers:
    _file_handler = logging.FileHandler(_logs_dir / "masks.log", mode="w", encoding="utf-8")
    _file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    _file_handler.setFormatter(_file_formatter)
    _logger.addHandler(_file_handler)
_logger.setLevel(logging.DEBUG)
_logger.propagate = False

def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX.
    :param card_number: Номер карты (16 цифр)
    :return: Маскированная строка
    """
    if len(card_number) < 6:
        _logger.error("Card number too short to mask: length=%d", len(card_number))
        return card_number  # Возвращаем как есть для коротких номеров

    _logger.debug("Masking card number of length %d", len(card_number))
    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    _logger.debug("Masked card number result ends with %s", card_number[-4:])
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта в формате **XXXX.
    :param account_number: Номер счёта
    :return: Маскированная строка
    """
    if not account_number:
        _logger.error("Empty account number provided")
        return ""

    if len(account_number) < 4:
        _logger.error("Account number too short to mask: length=%d", len(account_number))
        return f"**{account_number}"

    _logger.debug("Masking account number of length %d", len(account_number))
    masked = f"**{account_number[-4:]}"
    _logger.debug("Masked account ends with %s", account_number[-4:])
    return masked
