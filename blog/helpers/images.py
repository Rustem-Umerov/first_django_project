from typing import Any, Optional, cast

from django.db.models.fields.files import FieldFile


def compare_old_and_new_file(instance: Any, field_name: str) -> Optional[FieldFile]:
    """
    Возвращает старый файл, если он существует и отличается от нового.
    Иначе возвращает None.

    :param instance: Объект модели у которой есть поле image
    :param field_name: Строковое название поля FileField / ImageField
    """

    # Если объект создаётся впервые — старого файла нет
    if not instance.pk:
        return None

    # Определяем класс модели
    model = instance.__class__

    # Новый файл, который пользователь загрузил
    new_file = cast(Optional[FieldFile], getattr(instance, field_name, None))

    # Проверяем, что новый файл есть
    if not new_file:
        return None

    # Получаем старый объект модели из базы
    try:
        old_instance = model.objects.get(pk=instance.pk)
    except model.DoesNotExist:
        return None

    # Старый файл из базы данных
    old_file = cast(Optional[FieldFile], getattr(old_instance, field_name, None))

    # Проверяем, что старый файл есть
    if not old_file:
        return None

    # Если старый файл существует и он отличается от нового - возвращаем старый файл
    if old_file and old_file != new_file:
        return old_file
    return None
