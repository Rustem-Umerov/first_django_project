from typing import Protocol

from django.db.models.fields.files import FieldFile


class HasImageField(Protocol):
    """Описание интерфейса, то есть набора атрибутов, которые должны быть у объекта"""

    image: FieldFile
    pk: int
