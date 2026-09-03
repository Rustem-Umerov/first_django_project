from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self) -> None:
        """
        Расширение AppConfig:
            - импорт сигналов
        """

        import blog.signals  # noqa: F401
