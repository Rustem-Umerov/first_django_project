from typing import Any

from blog.models import BlogPost
from core.services.email_service import EmailService

from ..models import Event

# В этом модуле функции для работы с постом (BlogPost)


def function_that_collects_post_data(
    event: Event, content_object: BlogPost
) -> dict[str, Any]:
    """
    Собирает данные для письма, о том, что количество просмотров поста (объект BlogPost) = 100.

    :param event: Объект события (Event)
    :param content_object: Объект поста (BlogPost)
    :return: Словарь с данными
    """

    author_email = content_object.author.email
    author_name = content_object.author.username
    title_post = content_object.title
    count_views = content_object.count_views
    post_id = content_object.pk

    time_event = event.created_at
    event_type = event.event_type

    post_url = f"/blog/{post_id}/"

    return {
        "author_email": author_email,
        "author_name": author_name,
        "title_post": title_post,
        "count_views": count_views,
        "post_id": post_id,
        "time_event": time_event,
        "event_type": event_type,
        "post_url": post_url,
    }


def wrapper_post_reached_100_views(context: dict[str, Any]) -> int:
    """
    Отправляет письмо автору поста, когда пост достиг 100 просмотров.
    Wrapper-функция: готовит данные и вызывает EmailService.

    :param context: Данные для письма
    :return: Количество отправленных сообщений
    """

    # 1. Тема письма
    title_post = context["title_post"]
    subject = f"Ваш пост «{title_post}» набрал 100 просмотров."

    # 2. Шаблоны
    template_html = "emails/post_reached_100_views.html"
    template_txt = "emails/post_reached_100_views.txt"

    # 3. Получатель
    to_email = context["author_email"]

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
