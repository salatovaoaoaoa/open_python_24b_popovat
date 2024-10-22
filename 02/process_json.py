import json
from typing import Callable


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens_find: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:

    if required_keys is None or not required_keys:
        raise ValueError("Список ключей для поиска не задан или пуст")
    if tokens_find is None or not tokens_find:
        raise ValueError("Список токенов для поиска не задан или пуст")
    if callback is None:
        raise ValueError("Callback функция не задана")

    try:
        json_obj = json.loads(json_str)
    except json.JSONDecodeError as err:
        raise ValueError(f"Ошибка в формате JSON строки: {err}") from err

    lower_tokens_find = {token.lower() for token in tokens_find}

    for key in set(required_keys):
        value = json_obj.get(key, None)
        if value is None:
            continue
        lower_value = value.lower()
        for token in lower_tokens_find:
            if token in lower_value:
                callback(key, token)
