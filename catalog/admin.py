from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest

from .models import Category, Contact, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")
    list_display_links = ("name",)

    def save_model(
        self, request: HttpRequest, obj: Product, form: ModelForm, change: bool
    ) -> None:
        """
        Переопределение метода, для того чтобы сначала сохранить объект без фото, если оно есть.
        Для чего это нужно? Дело в том, что фото объекта должно быть сохранено в папку с названием номера pk объекта.
        Проблема в том, что если объект новый, то во время его создания pk еще нет,
        pk появится уже после создания объекта.
        Поэтому мы сохраняем объект без фото. Потом, когда pk появится, мы добавляем в объект фото.

        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """

        # Если объект новый (создаётся впервые)
        if not obj.pk:
            # Забираем файл из формы
            image = form.cleaned_data.get("image")

            # Временно убираем файл с объекта
            obj.image = None

            # Сначала сохраняем объект без файла и появится pk
            super().save_model(request, obj, form, change)

            if image:
                obj.image = image
                obj.save()
        else:
            # Если объект редактируется — обычное сохранение
            super().save_model(request, obj, form, change)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("id", "name", "phone", "email")
    search_fields = ("name", "phone", "email", "address")
    list_display_links = ("name",)
