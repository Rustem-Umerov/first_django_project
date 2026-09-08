from typing import Optional


def validate_bad_words(
    *, value: str, bad_words: list[str]
) -> tuple[bool, Optional[str]]:
    """
    Проверяет наличие запрещенных слов в строке.

    :param value: Строка для поиска.
    :param bad_words: Список запрещенных слов.
    :return: (True, слово) если найдено запрещённое слово, иначе (False, None)
    """

    normalized_value = value.casefold().strip()

    for word in bad_words:
        normalized_word = word.casefold().strip()
        if normalized_word in normalized_value:
            return True, word

    return False, None
