from typing import Any

from blog.models import BlogPost

from ..models import Event


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

    human_message = f"Ваш пост «{title_post}» набрал 100 просмотров."
    post_url = f"/blog/{post_id}/"

    return {
        "author_email": author_email,
        "author_name": author_name,
        "title_post": title_post,
        "count_views": count_views,
        "post_id": post_id,
        "time_event": time_event,
        "event_type": event_type,
        "human_message": human_message,
        "post_url": post_url,
    }
