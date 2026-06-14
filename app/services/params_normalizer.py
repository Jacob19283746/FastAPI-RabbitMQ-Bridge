async def normalize_query_params(items: list) -> dict:
    """Функция нормализации параметров запроса
        - Удаляет пробелы в начале и конце ключей/значений
        - Объединение значений с одинаковыми именами
        - Игнорирует пустые значения.
    Возвращает словарь с параметрами
    """
    normalized: dict = {}
    for key, value in items:
        clean_key = key.strip() if key else ""
        if not clean_key:
            continue
        clean_value = value.strip() if value else ""
        if not clean_value or clean_value in ['""', "''", '" "', "' '"]:
            continue
        existing = normalized.get(clean_key)
        if existing is None:
            normalized[clean_key] = clean_value
        elif isinstance(existing, list):
            existing.append(clean_value)
        else:
            normalized[clean_key] = [existing, clean_value]
    return normalized


if __name__ == "__main__":
    import asyncio
    print(asyncio.run(normalize_query_params(items=[("tag", " ")])))
