from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = "events"

    def ready(self) -> None:
        """
        Расширение AppConfig:
            - импорт сигналов
        """

        import events.signals  # noqa: F401
