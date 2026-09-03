from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Product


def product_image_path(instance: "Product", filename: str) -> str:
    """
    Формирует путь к месту хранения файла для модели Product

    :param instance: Объект модели Product
    :param filename: Название файл
    :return: Путь к месту хранения файла
    """

    return f"catalog/products/{instance.pk}/{filename}"
