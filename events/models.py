from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .enums import EventType


class Event(models.Model):
    """Фиксирует определенные событие для любых сущностей."""

    # К какой модели относится событие (BlogPost и т. д.)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name="Тип сущности"
    )

    # ID конкретного объекта (post.id, profile.id и т.д.)
    object_id = models.PositiveIntegerField(verbose_name="ID объекта")

    # Связка content_type + object_id → реальный объект
    content_object = GenericForeignKey("content_type", "object_id")

    # Тип события (что произошло?)
    event_type = models.CharField(
        max_length=100, choices=EventType.choices(), verbose_name="Тип события"
    )

    # Когда событие произошло
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата события")

    # Обработано ли событие (например, отправлено письмо)
    processed = models.BooleanField(default=False, verbose_name="Обработано (да/нет)")

    # Когда событие обработано (изначально пусто)
    processed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата обработки"
    )

    def __str__(self) -> str:
        return f"{self.event_type} — {self.content_type} #{self.object_id}"
