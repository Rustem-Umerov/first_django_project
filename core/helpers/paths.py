from pathlib import Path
from typing import Optional

from django.db.models.fields.files import FieldFile


def get_folder_path(field_file: FieldFile) -> Optional[Path]:
    """
    Возвращает путь к папке, в которой лежит файл.

    :param field_file: Объект файла
    """

    try:
        file_path = Path(field_file.path)
    except (ValueError, TypeError, FileNotFoundError):
        return None

    return file_path.parent
