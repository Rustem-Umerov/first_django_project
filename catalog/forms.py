from decimal import Decimal
from typing import Optional

from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile

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
            "name": forms.TextInput(attrs={"id": "id_name", "class": "form-control"}),
            "description": forms.Textarea(
                attrs={"id": "id_description", "class": "form-control"}
            ),
            "image": forms.ClearableFileInput(
                attrs={"id": "id_image", "class": "form-control"}
            ),
            "category": forms.Select(
                attrs={"id": "id_category", "class": "form-select"}
            ),
            "price": forms.NumberInput(
                attrs={"id": "id_price", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        """Добавляет Bootstrap‑классы к виджетам формы для единообразной стилизации полей."""

        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите имя"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите описание"}
        )
        self.fields["image"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.fields["category"].widget.attrs.update(
            {
                "class": "form-select",
            }
        )
        self.fields["price"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Укажите цену"}
        )

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
        """Валидирует фото продукта: проверяет размер и MIME‑тип."""

        image = self.cleaned_data.get("image")

        if image is None:
            return image

        # Проверка размера файла (5 МБ)
        max_size = 5_242_880  # 5 * 1024 * 1024
        if image.size > max_size:
            raise ValidationError(
                "Превышен максимальный размер фото продукта. Максимальный размер 5 242 880 байт."
            )

        # Проверка MIME‑типа (формат файла)
        content_type = image.file.content_type
        allowed_types = {"image/jpeg", "image/png"}
        if content_type not in allowed_types:
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
