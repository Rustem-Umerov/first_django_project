from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    def ready(self) -> None:
        """
        Расширение AppConfig:
            - импорт сигналов
        """

        import users.signals  # noqa: F401
