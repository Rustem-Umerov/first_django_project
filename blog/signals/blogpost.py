from typing import Any

from django.db import transaction
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from core.helpers.files import delete_file, delete_folder
from core.helpers.images import get_old_and_new_file
from core.helpers.paths import get_folder_path

from ..models import BlogPost


@receiver(post_delete, sender=BlogPost)
def delete_image_after_delete_post(
    sender: Any, instance: BlogPost, **kwargs: Any
) -> None:
    """
    При удалении объекта BlogPost:
    - удаляем файл изображения
    - удаляем папку с названием (pk), если она безопасна
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
def prepare_old_image_for_deletion(
    sender: Any, instance: BlogPost, **kwargs: Any
) -> None:
    """Запоминаем старое изображение, которое нужно удалить после сохранения."""

    # Если Django загружает фикстуры (loaddata), то сигнал должен быть отключён
    if kwargs.get("raw"):
        return

    # Если объект создаётся впервые — старого файла нет
    if instance._state.adding:
        return

    # Получаем список полей для обновления. Если нет списка или в нем нет поля "image", то возвращаем None
    update_fields = kwargs.get("update_fields")
    if update_fields is not None and "image" not in update_fields:
        return None

    # Получаем старый и новый файл.
    result = get_old_and_new_file(instance, "image")
    if result is None:
        return None

    old_image, new_image = result

    # Формируем путь к файлу, если есть новый файл.
    folder_path = get_folder_path(old_image) if new_image is None else None

    # Добавляем в объект атрибут.
    setattr(instance, "_image_cleanup_data", (old_image, folder_path))


@receiver(post_save, sender=BlogPost)
def delete_old_image_after_save(sender: Any, instance: BlogPost, **kwargs: Any) -> None:
    """Удаляем старое изображение после успешного сохранения BlogPost."""

    # Если Django загружает фикстуры (loaddata), то сигнал должен быть отключён
    if kwargs.get("raw"):
        return

    # Если атрибута _image_cleanup_data нет, то данных для удаления нет.
    cleanup_data = getattr(instance, "_image_cleanup_data", None)
    if cleanup_data is None:
        return None

    # Сразу удаляем атрибут.
    delattr(instance, "_image_cleanup_data")

    old_image, folder_path = cleanup_data
    obj_id = instance.pk

    def _cleanup() -> None:
        # Сначала удаляем файл через Django-хранилище
        delete_file(old_image)

        if folder_path:
            # Затем удаляем папку поста
            delete_folder(folder_path, obj_id)

    transaction.on_commit(_cleanup)
