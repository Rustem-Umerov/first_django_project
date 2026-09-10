from typing import Optional, cast

from django import forms
from django.db.models.fields.files import ImageFieldFile

from core.helpers.files import delete_file, delete_folder
from core.helpers.paths import get_folder_path

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

    def clean_image(self) -> Optional[ImageFieldFile]:
        """
        Валидирует фото продукта: если пользователь поставил галочку Clear(на сайте), то файл и папка будут удалены.
        """

        image = self.cleaned_data.get("image")

        # Пользователь поставил галочку "Clear"
        if image is False:
            # Получаем путь к папке ДО удаления файла
            folder_path = get_folder_path(self.instance.image)
            if folder_path is None:
                raise ValueError("Путь к папке определить не удалось.")

            # Удаляем файл
            delete_file(self.instance.image)

            # Удаляем папку
            delete_folder(folder_path, self.instance.pk)

            return None

        if image is None:
            return image

        return cast(ImageFieldFile, image)
