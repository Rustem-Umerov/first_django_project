from typing import Any, Callable

from django.utils import timezone

from .handlers.post_handlers import (
    function_that_collects_post_data,
    wrapper_post_reached_100_views,
)
from .models import Event


class EventHandler:
    """
    Класс-обработчик событий.
    В зависимости от типа события, вызывает подходящую функцию для сборки контекста данных для письма.
    Далее, в зависимости от типа события, вызывает wrapper‑функцию для отправки письма.
    """

    # Словарь {тип события: функция для сборки контекста}
    EVENT_TYPE_DICT_AND_CONTEXT_COLLECTOR = {
        "post_reached_100_views": function_that_collects_post_data
    }

    # Словарь {тип события: функция-обертка для отправки письма}
    EVENT_TYPE_DICT_AND_WRAPPER_FOR_SENDING = {
        "post_reached_100_views": wrapper_post_reached_100_views
    }

    # Название класса (например, для логов)
    HANDLER_NAME = "EventHandler"

    def __init__(
        self,
        event: Event,
        max_attempts: int = 3,
    ) -> None:
        """
        Инициализирует обработчик события.

        Сохраняет объект события, связанный content_object, сервис отправки писем
        и логгер. Подготавливает структуру для контекста и флаг обработки.
        """

        self.event: Event = event
        self.max_attempts = max_attempts
        self.content_object: Any = event.content_object
        self.context: dict[str, Any] = {}

    def _get_function(
        self, mapping_dick: dict[str, Callable[..., Any]]
    ) -> Callable[..., Any]:
        """
        Определяет правильную функцию в зависимости от типа события.

        :param mapping_dick: Словарь {тип_события: функция}
        :return: Функцию.
        """

        event_type = self.event.event_type

        function = mapping_dick.get(event_type)
        if function is None:
            raise ValueError(
                f"{self.HANDLER_NAME} не умеет обрабатывать событие: {event_type}"
            )
        return function

    def prepare(self) -> None:
        """
        Готовит контекст для отправки письма.
        Вызывает функцию-обработчик, соответствующую event_type.
        """

        event_type = self.event.event_type

        # Определяет правильную функцию, для сбора контекста.
        handler_function = self._get_function(
            self.EVENT_TYPE_DICT_AND_CONTEXT_COLLECTOR
        )

        try:
            self.context = handler_function(self.event, self.content_object)
        except Exception as exc:
            raise Exception(
                f"{self.HANDLER_NAME}: ошибка при подготовке контекста "
                f"для события {event_type}"
            ) from exc

    def send(self) -> int:
        """
        Выбирает правильную wrapper-функцию и отправляет письмо.

        :return: Количество отправленных писем
        """

        # Определяет правильную функцию, для отправки письма.
        wrapper_function = self._get_function(
            self.EVENT_TYPE_DICT_AND_WRAPPER_FOR_SENDING
        )

        sent_count: int = wrapper_function(context=self.context)
        return sent_count

    def mark_processed(self) -> None:
        """Отмечает событие как обработанное."""

        self.event.processed = True
        self.event.processed_at = timezone.now()
        self.event.save(update_fields=["processed", "processed_at"])

    def handle(self) -> int:
        """
        Главный метод. Запускает весь процесс обработки события.
        Вызывает prepare() - вызывает send() - вызывает mark_processed()
        Делает max_attempts попыток отправки письма.
        Если хотя бы одна успешна — событие помечается как обработанное.

        :return: Результат отправки
        """

        # 1. Собирает контекст
        self.prepare()

        # 2. Отправка письма
        for attempt in range(self.max_attempts):
            sent_count = self.send()

            if sent_count > 0:
                # 3. Отмечает событие как обработанное
                self.mark_processed()

                # 4. Возврат результата отправки
                return sent_count

        raise Exception(f"Письмо не отправлено после {self.max_attempts} попыток")
