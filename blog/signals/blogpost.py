from typing import Any

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from ..helpers.files import delete_file, delete_folder
from ..helpers.images import compare_old_and_new_file
from ..helpers.paths import get_folder_path
from ..models import BlogPost


@receiver(post_delete, sender=BlogPost)
def delete_image_after_delete_post(
    sender: type[Any], instance: Any, **kwargs: Any
) -> None:
    """
    При удалении объекта BlogPost:
    - удаляем файл изображения
    - удаляем папку и изображением (pk), если она безопасна
    """

    if not instance.image:
        return

    # Получаем путь к папке до удаления файла
    folder_path = get_folder_path(instance.image)

    # Определяем id объекта до удаления файла
    obj_id = instance.pk

    # Сначала удаляем файл через Django-хранилище
    delete_file(instance.image)

    # Затем удаляем папку поста
    delete_folder(folder_path, obj_id)


@receiver(pre_save, sender=BlogPost)
def delete_old_image_after_update_post_image(
    sender: type[Any], instance: Any, **kwargs: Any
) -> None:
    """Удаляем старое фото поста при обновлении фото у объекта BlogPost"""

    # Если объект создаётся впервые — старого файла нет
    if not instance.pk:
        return

    old_image = compare_old_and_new_file(instance, "image")
    if old_image:
        delete_file(old_image)
