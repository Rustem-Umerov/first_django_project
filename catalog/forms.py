from decimal import Decimal
from typing import Optional

import django_filters
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile
from PIL import Image, UnidentifiedImageError

from core.validators import validate_bad_words

from .models import Product

BAD_WORD = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продуктов.
    Основана на модели Product.
    """

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "image",
            "category",
            "price",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите имя"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Введите описание"}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Укажите цену"}
            ),
        }

    def clean_name(self) -> str:
        """Проверяет наличие запрещенных слов в поле 'name'"""

        name = self.cleaned_data.get("name")
        if name is None:
            raise ValidationError("Поле 'name' не прошло проверку.")

        bool_value, bad_word = validate_bad_words(value=name, bad_words=BAD_WORD)

        if bool_value:
            raise ValidationError(f"В поле 'name' есть запрещенное слово '{bad_word}'.")

        return name

    def clean_description(self) -> str:
        """Проверяет наличие запрещенных слов в поле 'description'"""

        description = self.cleaned_data.get("description")
        if description is None:
            raise ValidationError("Поле 'description' не прошло проверку.")

        bool_value, bad_word = validate_bad_words(value=description, bad_words=BAD_WORD)

        if bool_value:
            raise ValidationError(
                f"В поле 'description' есть запрещенное слово '{bad_word}'."
            )

        return description

    def clean_image(self) -> Optional[ImageFieldFile]:
        """Валидирует фото продукта: проверяет размер и формат файла."""

        image = self.cleaned_data.get("image")

        # Проверка: None - фото вообще не передали, False - пользователь нажал Clear.
        if image is None or image is False:
            return image

        # Проверка размера файла (5 МБ)
        max_size = 5_242_880  # 5 * 1024 * 1024
        if image.size > max_size:
            raise ValidationError(
                "Превышен максимальный размер фото продукта. Максимальный размер 5 242 880 байт."
            )

        # Проверка формата файла
        try:
            img = Image.open(image)
            img_format = img.format.lower()

        except UnidentifiedImageError:
            raise ValidationError("Файл не является изображением.")
        except OSError:
            raise ValidationError("Файл повреждён или имеет неверный формат.")
        except Exception:
            raise ValidationError("Не удалось обработать изображение.")

        if img_format not in {"jpeg", "png"}:
            raise ValidationError("Допустимы только JPEG и PNG.")

        return image

    def clean_price(self) -> Decimal:
        """Проверяет, что цена НЕ отрицательная."""

        price = self.cleaned_data.get("price")

        if price is None:
            raise ValidationError("Поле 'price' не прошло проверку.")

        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")

        return price


class ProductAdminForm(ProductForm):
    """
    Форма для создания и редактирования продуктов для админки.
    Наследуется от ProductForm и добавляет поле статуса.
    """

    class Meta(ProductForm.Meta):
        # Берем список полей родителя и добавляем новое
        fields = ProductForm.Meta.fields + [
            "status",
        ]

        widgets = {
            **ProductForm.Meta.widgets,
            "status": forms.Select(attrs={"id": "id_status", "class": "form-select"}),
        }


class ProductFilter(django_filters.FilterSet):
    """
    Форма для валидации фильтров. Если пользователь хочет отфильтровать объекты Product.
    """

    class Meta:
        model = Product
        fields = ["status"]
