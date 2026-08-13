from enum import Enum


class EventType(Enum):
    """
    Enum-класс, который содержит все допустимые типы событий.
    Каждый элемент — это фиксированная константа.
    """

    POST_REACHED_100_VIEWS = "post_reached_100_views"  # Пост достиг 100 просмотров.

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        """
        Возвращает список кортежей (value, label),
        который Django использует в choices.
        """

        return [(item.value, item.name.replace("_", " ").title()) for item in cls]
