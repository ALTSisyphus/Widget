"""Утилиты для чтения JSON-файлов.

Этот модуль содержит функцию read_json_file, которая безопасно читает
JSON-файл и возвращает список словарей. Если файл отсутствует, пуст,
или содержит не-список — возвращается пустой список.

"""

    if not path:
        return []

    # Попытка открыть и прочитать файл
    try:
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
            # Если файл пустой (только пробельные символы) — вернуть пустой список
            if not content.strip():
                return []
            data = json.loads(content)
            # Если содержимое JSON не является списком — вернуть пустой список
            if not isinstance(data, list):
                return []
            return data
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        # Любая указанная ошибка чтения/парсинга преобразуется в пустой список

        return []