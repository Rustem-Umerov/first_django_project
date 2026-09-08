from django import forms
from django.core.exceptions import ValidationError

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
