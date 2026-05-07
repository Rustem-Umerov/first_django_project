from django import forms

from .models import Product


class ProductForm(forms.ModelForm[Product]):
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
