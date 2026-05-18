from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import BlogPost


def blogpost_image_path(instance: "BlogPost", filename: str) -> str:
    """
    Формирует путь к месту хранения файла для модели BlogPost

    :param instance: Объект модели BlogPost
    :param filename: Название файл
    :return: Путь к месту хранения файла
    """

    return f"blog/blogpost/{instance.pk}/{filename}"
