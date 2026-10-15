from typing import Any

from core.services.email_service import EmailService
from users.models import CustomUser

from ..models import Event

# В этом модуле функции для работы c CustomUser


def function_that_collects_user_data(
    event: Event, content_object: CustomUser
) -> dict[str, Any]:
    """
    Собирает данные для приветственного письма пользователю после регистрации.

    :param event: Объект события (Event)
    :param content_object: Объект CustomUser
    :return: Словарь с данными
    """

    username = content_object.username
    user_email = content_object.email

    time_event = event.created_at
    event_type = event.event_type

    return {
        "username": username,
        "user_email": user_email,
        "time_event": time_event,
        "event_type": event_type,
    }


def wrapper_user_registered(context: dict[str, Any]) -> int:
    """
    Отправляет письмо пользователю после регистрации.
    Wrapper-функция: готовит данные и вызывает EmailService.

    :param context: Данные для письма
    :return: Количество отправленных сообщений
    """

    # 1. Тема письма
    username = context["username"]
    subject = (
        f"Добро пожаловать на наш сайт, {username}!!! Вы успешно зарегистрировались!!!"
    )

    # 2. Шаблоны
    template_html = "emails/user_has_registered.html"
    template_txt = "emails/user_has_registered.txt"

    # 3. Получатель
    to_email = context["user_email"]

    # Если нет адреса получателя, то отправка не возможна
    if not to_email:
        return 0

    # 4. Дополнительные параметры
    attachments = None
    reply_to = None

    # 5. Создание сервиса отправки (EmailService)
    email_service = EmailService()

    # 6. Вызов отправки письма
    sent_count = email_service.send(
        to_email=to_email,
        subject=subject,
        template_html=template_html,
        template_txt=template_txt,
        context=context,
        attachments=attachments,
        reply_to=reply_to,
    )
    return sent_count or 0
