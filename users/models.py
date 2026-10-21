from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(verbose_name="Электронная почта", unique=True)

    def get_avatar_path(self, filename: str) -> str:
        """
        Формирует путь к месту хранения файла для модели CustomUser

        :param filename: Название файл
        :return: Путь к месту хранения файла
        """

        return f"avatars/{self.pk}/{filename}"

    avatar = models.ImageField(
        verbose_name="Аватар", upload_to=get_avatar_path, blank=True
    )
    phone_number = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        blank=True,
        help_text="Введите номер телефона",
    )
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        blank=True,
        help_text="Введите название вашей страны",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def avatar_url(self) -> str:
        """
        Возвращает avatar если файл есть, иначе возвращает дефолтный аватар.
        """

        if self.avatar:
            return self.avatar.url
        return settings.DEFAULT_AVATAR_URL

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"
