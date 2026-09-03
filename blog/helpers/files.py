import shutil
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.db.models.fields.files import FieldFile


def delete_file(file_field: FieldFile) -> None:
    """
    Функция для удаления файла

    :param file_field: Объект файла
    """

    if file_field:
        file_field.delete(save=False)


def is_safe_post_folder(path: Optional[Path], obj_id: int) -> bool:
    """
    Проверяет, что папка действительно принадлежит этому посту
    и находится внутри MEDIA_ROOT.
    """

    # 1. Папка должна существовать и быть директорией
    if not path or not path.exists() or not path.is_dir():
        return False

    # 2. Имя папки должно совпадать с pk объекта
    if path.name != str(obj_id):
        return False

    # 3. Папка должна находиться внутри MEDIA_ROOT
    media_root = Path(settings.MEDIA_ROOT).resolve()
    path_resolved = path.resolve()

    # Проверяем, что path_resolved начинается с media_root
    return media_root in path_resolved.parents


def delete_folder(folder_path: Optional[Path], obj_id: int) -> None:
    """
    Удаляет папку поста целиком, если она безопасна для удаления.
    """

    if folder_path is None:
        return

    if is_safe_post_folder(folder_path, obj_id):
        shutil.rmtree(folder_path, ignore_errors=False)
