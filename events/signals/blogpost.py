from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import BlogPost

from ..event_handlers import EventHandler
from ..services import handle_post_view_event


@receiver(post_save, sender=BlogPost)
def blogpost_saved(sender: Any, instance: BlogPost, **kwargs: Any) -> None:
    """
    Проверяет объект поста(BlogPost), если количество просмотров = 100 и события: "Пост достиг 100 просмотров" в базе
    данных Event нет, то происходит обработка события - отправка письма.

    :param sender: Модель BlogPost
    :param instance: Объект поста (BlogPost)
    """

    if instance.count_views == 100:
        event_created = handle_post_view_event(instance)
        if event_created:
            # Если объект Event создан, создается обработчик события EventHandler
            handler = EventHandler(event=event_created)
            handler.handle()
