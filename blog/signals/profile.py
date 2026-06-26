from typing import Any

from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from ..helpers.files import delete_file, delete_folder
from ..helpers.images import compare_old_and_new_file
from ..helpers.paths import get_folder_path
from ..models import Profile


@receiver(signal=post_save, sender=User)
def create_profile(
    sender: type[Any], instance: Any, created: bool, **kwargs: Any
) -> None:
    """Создает объект Profile для объекта User"""

    if created:
        Profile.objects.create(user=instance)


@receiver(signal=post_delete, sender=Profile)
def delete_avatar_after_delete_profile(
    sender: type[Any], instance: Any, **kwargs: Any
) -> None:
    """
    При удалении объекта Profile:
    - удаляем аватар профиля
    - удаляем папку с аватаркой (pk), если она безопасна
    """

    if not instance.avatar:
        return

    # Получаем путь к папке до удаления файла
    folder_path = get_folder_path(instance.avatar)

    # Определяем id объекта до удаления файла
    obj_id = instance.pk

    # Сначала удаляем файл через Django-хранилище
    delete_file(instance.avatar)

    # Затем удаляем папку поста
    delete_folder(folder_path, obj_id)


@receiver(pre_save, sender=Profile)
def delete_old_image_after_update_post_image(
    sender: type[Any], instance: Any, **kwargs: Any
) -> None:
    """Удаляем старую аватарку при обновлении фото у объекта Profile"""

    # Если объект создаётся впервые — старого файла нет
    if not instance.pk:
        return

    old_avatar = compare_old_and_new_file(instance, "avatar")
    if old_avatar:
        delete_file(old_avatar)
