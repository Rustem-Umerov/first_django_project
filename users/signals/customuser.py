from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from core.helpers.files import delete_file, delete_folder
from core.helpers.images import compare_old_and_new_file
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
def delete_old_image_after_update_custom_user_image(
    sender: Any, instance: CustomUser, **kwargs: Any
) -> None:
    """Удаляем старую аватарку при обновлении фото у объекта CustomUser"""

    # Если Django загружает фикстуры (loaddata), то сигнал должен быть отключён
    if kwargs.get("raw"):
        return

    # Объект создаётся впервые — старого файла нет
    if instance._state.adding:
        return

    old_avatar = compare_old_and_new_file(instance, "avatar")
    if old_avatar:
        delete_file(old_avatar)


@receiver(pre_save, sender=CustomUser)
def delete_avatar_on_clear_for_custom_user(
    sender: Any, instance: CustomUser, **kwargs: Any
) -> None:
    """Удаляет аватарку, если пользователь в админке поставил галочку Clear на поле avatar для объекта CustomUser."""

    # Если Django загружает фикстуры (loaddata), то сигнал должен быть отключён
    if kwargs.get("raw"):
        return

    # Объект создаётся впервые - старой версии в базе нет, значит сравнивать нечего
    if instance._state.adding:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return

    # Папка, где лежит старый файл
    folder_path = get_folder_path(old_instance.avatar)

    # id пользователя, так как в названии папки значение CustomUser.pk
    obj_id = old_instance.pk

    # Если раньше файл был, а теперь поле пустое - пользователь нажал Clear
    if old_instance.avatar.name and not instance.avatar.name:
        old_instance.avatar.delete(save=False)

        # Затем удаляем папку поста
        delete_folder(folder_path, obj_id)
