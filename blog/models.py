from django.db import models

from .utils import blogpost_image_path


class BlogPost(models.Model):
    """Модель поста в блоге."""

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(
        upload_to=blogpost_image_path,
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
