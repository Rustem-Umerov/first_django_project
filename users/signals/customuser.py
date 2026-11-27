from typing import Any

from django.db import transaction
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from core.helpers.files import delete_file, delete_folder
from core.helpers.images import get_old_and_new_file
from core.helpers.paths import get_folder_path

from ..models import CustomUser


@receiver(signal=post_delete, sender=CustomUser)
def delete_avatar_after_delete_custom_user(
    sender: Any, instance: CustomUser, **kwargs: Any
) -> None:
    """
    При удалении объекта CustomUser:
    - удаляем аватар пользователя
    - удаляем папку с аватаркой (pk), если она безопасна
    """

    if not instance.avatar:
        return

    # Получаем путь к папке до удаления файла
    folder_path = get_folder_path(instance.avatar)

    # Определяем id пользователя до удаления файла
    obj_id = instance.pk

    # Сначала удаляем файл через Django-хранилище
    delete_file(instance.avatar)

    # Затем удаляем папку с аватаром пользователя
    delete_folder(folder_path, obj_id)


@receiver(pre_save, sender=CustomUser)
def prepare_old_avatar_for_deletion(
    sender: Any, instance: CustomUser, **kwargs: Any
) -> None:
    """Запоминаем старый avatar, который нужно удалить после сохранения."""

    # Если Django загружает фикстуры (loaddata), то сигнал должен быть отключён
    if kwargs.get("raw"):
        return

    # Если объект создаётся впервые — старого файла нет
    if instance._state.adding:
        return

    # Получаем список полей для обновления. Если нет списка или в нем нет поля "avatar", то возвращаем None
    update_fields = kwargs.get("update_fields")
    if update_fields is not None and "avatar" not in update_fields:
        return None

    # Получаем старый и новый файл.
    result = get_old_and_new_file(instance, "avatar")
    if result is None:
        return None

    old_avatar, new_avatar = result

    # Формируем путь к файлу, если есть новый файл.
    folder_path = get_folder_path(old_avatar) if new_avatar is None else None

    # Добавляем в объект атрибут.
    setattr(instance, "_avatar_cleanup_data", (old_avatar, folder_path))


@receiver(post_save, sender=CustomUser)
def delete_old_avatar_after_save(
    sender: Any, instance: CustomUser, **kwargs: Any
) -> None:
    """Удаляем старое изображение после успешного сохранения CustomUser."""

    # Если Django загружает фикстуры (loaddata), то сигнал должен быть отключён
    if kwargs.get("raw"):
        return

    # Если атрибута _avatar_cleanup_data нет, то данных для удаления нет.
    cleanup_data = getattr(instance, "_avatar_cleanup_data", None)
    if cleanup_data is None:
        return None

    # Сразу удаляем атрибут.
    delattr(instance, "_avatar_cleanup_data")

    old_avatar, folder_path = cleanup_data
    obj_id = instance.pk

    def _cleanup() -> None:
        # Сначала удаляем файл через Django-хранилище
        delete_file(old_avatar)

        if folder_path:
            # Затем удаляем папку поста
            delete_folder(folder_path, obj_id)

    transaction.on_commit(_cleanup)
