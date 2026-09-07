from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# from .helpers.paths import blogpost_image_path, profile_avatar_path


class BlogPost(models.Model):
    """Модель поста в блоге."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name="Автор",
    )

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")

    def get_image_path(self, filename: str) -> str:
        """
        Формирует путь к месту хранения файла для модели BlogPost

        :param filename: Название файл
        :return: Путь к месту хранения файла
        """

        return f"blog/blogpost/{self.pk}/{filename}"

    image = models.ImageField(
        upload_to=get_image_path,
        verbose_name="Изображение поста",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    is_published = models.BooleanField(verbose_name="Опубликовано", default=False)
    count_views = models.IntegerField(verbose_name="Количество просмотров", default=0)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """Если поле title больше, чем 50 символов, то обрезаем и добавляем ..."""

        title = self.title
        if len(title) > 50:
            title = title[:50] + "..."
        return title


class Profile(models.Model):
    """Модель профиля пользователя."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_avatar_path(self, filename: str) -> str:
        """
        Формирует путь к месту хранения файла для модели Profile

        :param filename: Название файл
        :return: Путь к месту хранения файла
        """

        return f"avatars/{self.user.pk}/{filename}"

    avatar = models.ImageField(upload_to=get_avatar_path, blank=True, null=True)
    nickname = models.CharField(max_length=50, unique=True)

    @property
    def avatar_url(self) -> str:
        """
        Возвращает avatar если файл есть, иначе возвращает дефолтный аватар.
        """

        if self.avatar:
            return self.avatar.url
        return settings.DEFAULT_AVATAR_URL

    def __str__(self) -> str:
        return self.nickname or self.user.username


class PostView(models.Model):
    """Показывает просмотры поста авторизованным пользователем и время просмотра."""

    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="views", verbose_name="Пост"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="post_views",
        verbose_name="Пользователь",
    )
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата просмотра")

    class Meta:
        unique_together = ("user", "post")

    def __str__(self) -> str:
        return f"{self.post} — {self.user} — {self.viewed_at}"
