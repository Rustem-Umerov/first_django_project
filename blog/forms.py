from django import forms

from .models import BlogPost


class BlogPostForm(forms.ModelForm):  # type: ignore[type-arg]
    """
    Форма для создания и редактирования продуктов.
    Основана на модели BlogPost.
    """

    class Meta:
        model = BlogPost
        fields = [
            "title",
            "content",
            "image",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите заголовок"}
            ),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        }
