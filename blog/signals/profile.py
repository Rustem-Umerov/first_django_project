from typing import Any

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from core.helpers.files import delete_file, delete_folder
from core.helpers.images import compare_old_and_new_file
from core.helpers.paths import get_folder_path

from ..models import Profile


@receiver(signal=post_save, sender=User)
def create_profile(sender: Any, instance: User, created: bool, **kwargs: Any) -> None:
    """Создает объект Profile для объекта User, если его еще нет."""

    # Проверка, что объект новый
    if not created:
        return None

    def _create_profile() -> None:
        """
        Если Inline форма создала объект Profile, то данная функция, просто, возвращает этот объект Profile.
        Если объект Profile не был создан раньше, то данная функция создает его.
        """

        Profile.objects.get_or_create(user=instance)

    transaction.on_commit(_create_profile)


@receiver(signal=post_delete, sender=Profile)
def delete_avatar_after_delete_profile(
    sender: Any, instance: Profile, **kwargs: Any
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
    obj_id = instance.user.pk

    # Сначала удаляем файл через Django-хранилище
    delete_file(instance.avatar)

    # Затем удаляем папку поста
    delete_folder(folder_path, obj_id)


@receiver(pre_save, sender=Profile)
def delete_old_image_after_update_profile_image(
    sender: Any, instance: Profile, **kwargs: Any
) -> None:
    """Удаляем старую аватарку при обновлении фото у объекта Profile"""

    # Если Django загружает фикстуры (loaddata), то сигнал должен быть отключён
    if kwargs.get("raw"):
        return

    # Объект создаётся впервые — старого файла нет
    if instance._state.adding:
        return

    old_avatar = compare_old_and_new_file(instance, "avatar")
    if old_avatar:
        delete_file(old_avatar)


@receiver(pre_save, sender=Profile)
def delete_avatar_on_clear(sender: Any, instance: Profile, **kwargs: Any) -> None:
    """Удаляет аватарку, если пользователь в админке поставил галочку Clear на поле avatar."""

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

    # id пользователя, то есть User.pk, а не Profile.pk, так как в названии папки значение User.pk
    obj_id = old_instance.user.pk

    # Если раньше файл был, а теперь поле пустое - пользователь нажал Clear
    if old_instance.avatar.name and not instance.avatar.name:
        old_instance.avatar.delete(save=False)

        # Затем удаляем папку поста
        delete_folder(folder_path, obj_id)
