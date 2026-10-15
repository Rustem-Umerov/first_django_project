from typing import Optional

from django.contrib.contenttypes.models import ContentType

from blog.models import BlogPost
from users.models import CustomUser

from .enums import EventType
from .models import Event


def handle_post_view_event(post: BlogPost) -> Optional[Event]:
    """
    Проверяет количество просмотров у поста.
    Проверяет не записано ли это событие в таблице Event.
    Если количество просмотров равно 100 и записи в таблице Event нет,
    то делает запись в таблицу Event.

    :param post: Объект поста (класс BlogPost).
    :return: Объект Event, если событие создано, иначе - None.
    """

    view_count = post.count_views

    if view_count != 100:
        return None

    if Event.objects.filter(
        content_type=ContentType.objects.get_for_model(post),
        object_id=post.pk,
        event_type=EventType.POST_REACHED_100_VIEWS.value,
    ).exists():
        return None

    return Event.objects.create(
        content_type=ContentType.objects.get_for_model(post),
        object_id=post.pk,
        event_type=EventType.POST_REACHED_100_VIEWS.value,
    )


def handle_user_registered_event(user: CustomUser) -> Optional[Event]:
    """
    Проверяет, не записано ли событие регистрации для этого пользователя в таблице Event.
    Если записи нет, то создает её.

    :param user: Объект пользователя (класс CustomUser).
    :return: Объект Event, если событие создано, иначе - None.
    """

    if Event.objects.filter(
        content_type=ContentType.objects.get_for_model(user),
        object_id=user.pk,
        event_type=EventType.USER_REGISTERED.value,
    ).exists():
        return None

    return Event.objects.create(
        content_type=ContentType.objects.get_for_model(user),
        object_id=user.pk,
        event_type=EventType.USER_REGISTERED.value,
    )
