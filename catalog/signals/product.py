from typing import Any

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from core.helpers.files import delete_file, delete_folder
from core.helpers.images import compare_old_and_new_file
from core.helpers.paths import get_folder_path

from ..models import Product


@receiver(post_delete, sender=Product)
def delete_image_after_delete_product(
    sender: Any, instance: Product, **kwargs: Any
) -> None:
    """
    При удалении объекта Product:
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


@receiver(pre_save, sender=Product)
def delete_old_image_after_update_product_image(
    sender: Any, instance: Product, **kwargs: Any
) -> None:
    """Удаляем старое фото продукта при обновлении фото у объекта Product"""

    # Если объект создаётся впервые — старого файла нет
    if instance._state.adding:
        return

    old_image = compare_old_and_new_file(instance, "image")
    if old_image:
        delete_file(old_image)
