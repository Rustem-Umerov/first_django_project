import logging
from typing import Any

from .handlers.post_handlers import function_that_collects_post_data
from .models import Event


class EventHandler:
    """
    Класс-обработчик событий.
    В зависимости от типа события, вызывает подходящую функцию для сборки контекста данных для письма.
    Далее, в зависимости от типа события, вызывает wrapper‑функцию для отправки письма.
    """

    # Словарь {тип события: функция для сборки контекста}
    EVENT_TYPE_DICT = {"post_reached_100_views": function_that_collects_post_data}

    # Название класса (например, для логов)
    HANDLER_NAME = "EventHandler"

    def __init__(
        self, event: Event, email_service: Any, logger: logging.Logger
    ) -> None:
        """
        Инициализирует обработчик события.

        Сохраняет объект события, связанный content_object, сервис отправки писем
        и логгер. Подготавливает структуру для контекста и флаг обработки.
        """

        self.event: Event = event
        self.content_object: Any = event.content_object
        self.email_service: Any = email_service
        self.logger: logging.Logger = logger
        self.context: dict[str, Any] = {}
        self.processed_flag: bool = False

    def prepare(self) -> None:
        """
        Готовит контекст для отправки письма.
        Вызывает функцию-обработчик, соответствующую event_type.
        """

        event_type = self.event.event_type

        handler_function = self.EVENT_TYPE_DICT.get(event_type)
        if handler_function is None:
            raise ValueError(
                f"{self.HANDLER_NAME} не умеет обрабатывать событие: {event_type}"
            )

        try:
            self.context = handler_function(self.event, self.content_object)
        except Exception as exc:
            self.logger.error(
                f"{self.HANDLER_NAME}: ошибка при подготовке контекста "
                f"для события {event_type}: {exc}"
            )
            raise
