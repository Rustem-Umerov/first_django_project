from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser

from ..event_handlers import EventHandler
from ..services import handle_user_registered_event


@receiver(signal=post_save, sender=CustomUser)
def user_registered_signal(
    sender: Any, instance: CustomUser, created: bool, **kwargs: Any
) -> None:
    """Отправляет приветственное письмо только при создании нового пользователя."""

    if created:
        event_created = handle_user_registered_event(instance)
        if event_created:
            handler = EventHandler(event=event_created)

            try:
                handler.handle()
            except Exception as e:
                print("\n[SIGNAL ERROR] Ошибка в сигнале 'user_registered_signal'")
                print(f"Детали ошибки:\n{e}\n")
