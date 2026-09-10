from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpRequest

from .forms import BlogPostForm
from .models import BlogPost, Profile
from .typing import UserWithProfile


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    form = BlogPostForm
    list_display = ("author", "title", "is_published", "created_at", "count_views")
    list_filter = ("author", "is_published", "created_at")
    search_fields = ("title", "content")
    ordering = ("-created_at",)

    def save_model(
        self, request: HttpRequest, obj: BlogPost, form: BlogPostForm, change: bool
    ) -> None:
        """
        Переопределение метода, для того чтобы сначала сохранить объект без фото, если оно есть.
        Для чего это нужно? Дело в том, что фото объекта должно быть сохранено в папку с названием номера pk объекта.
        Проблема в том, что если объект новый, то во время его создания pk еще нет,
        pk появится уже после создания объекта.
        Поэтому мы сохраняем объект без фото. Потом, когда pk появится, мы добавляем в объект фото.

        :param request: Текущий HTTP‑запрос из админки
        :param obj: экземпляр модели BlogPost, который сохраняется
        :param form: форма, содержащая обработанные данные и cleaned_data
        :param change: флаг, показывающий, редактируется объект или создаётся впервые
        :return: None
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


# ==================================================================
# ========== Интегрируем модель Profile в класс UserAdmin ==========


class ProfileInline(admin.StackedInline):  # type: ignore[type-arg]
    model = Profile
    can_delete = False
    extra = 0
    verbose_name_plural = "Профиль пользователя"


class CustomUserAdmin(UserAdmin):  # type: ignore[type-arg]
    inlines = (ProfileInline,)

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "profile_nickname",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "profile__nickname",
    )
    ordering = ("username", "profile__nickname")

    @admin.display(description="Nickname")
    def profile_nickname(self, obj: UserWithProfile) -> str:
        return obj.profile.nickname


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# ==================================================================
# ==================================================================
