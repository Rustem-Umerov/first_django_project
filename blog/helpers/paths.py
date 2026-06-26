from pathlib import Path
from typing import TYPE_CHECKING, Optional

from django.db.models.fields.files import FieldFile

if TYPE_CHECKING:
    from ..models import BlogPost, Profile


def blogpost_image_path(instance: "BlogPost", filename: str) -> str:
    """
    Формирует путь к месту хранения файла для модели BlogPost

    :param instance: Объект модели BlogPost
    :param filename: Название файл
    :return: Путь к месту хранения файла
    """

    return f"blog/blogpost/{instance.pk}/{filename}"


def profile_avatar_path(instance: "Profile", filename: str) -> str:
    """
    Формирует путь к месту хранения файла для модели Profile

    :param instance: Объект модели Profile
    :param filename: Название файл
    :return: Путь к месту хранения файла
    """

    return f"avatars/{instance.user.pk}/{filename}"


def get_folder_path(field_name: FieldFile) -> Optional[Path]:
    """
    Возвращает путь к папке, в которой лежит файл.

    :param field_name: Объект файла
    """

    try:
        file_path = Path(field_name.path)
    except (ValueError, TypeError, FileNotFoundError):
        return None

    return file_path.parent
