from typing import Any, Optional, cast

from django.db.models.fields.files import FieldFile


def get_old_and_new_file(
    instance: Any, field_name: str
) -> Optional[tuple[FieldFile, Optional[FieldFile]]]:
    """
    Если старый файл, то возвращает старый и новый файл.
    При этом новый файл может отсутствовать. Это означает что нужно, просто, удалить файл из объекта.
    Иначе возвращает None.

    :param instance: Объект модели у которой есть поле image
    :param field_name: Строковое название поля FileField / ImageField
    """

    # Объект создаётся впервые — старого файла нет
    if instance._state.adding:
        return None

    # Определяем класс модели
    model = instance.__class__

    # Новый файл, который пользователь загрузил
    new_file = cast(Optional[FieldFile], getattr(instance, field_name, None))

    # Получаем старый объект модели из базы
    try:
        old_instance = model.objects.get(pk=instance.pk)
    except model.DoesNotExist:
        return None

    # Старый файл из базы данных
    old_file = cast(Optional[FieldFile], getattr(old_instance, field_name, None))

    # Проверяем, что старый файл есть. Если нет, то возвращаем None, так удалять нечего.
    if not old_file or not old_file.name:
        return None

    # Если нового файла нет, то, просто, нужно оставить объект без файла.
    # Возвращаем (старый файл, новый файл) чтобы можно было проверить есть ли новый файл, если нет,
    # то нужно удалить и старый файл и папку.
    if new_file is None or not new_file.name:
        return old_file, None

    # Проверка новый файл или нет через флаг _committed
    # (_committed = False - файл не сохранен в storage, _committed = True - файл сохранен в storage)
    if not new_file._committed:  # type: ignore[attr-defined]
        return old_file, new_file
    return None
