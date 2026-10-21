from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  # type: ignore[type-arg]
    list_display = ("username", "email", "phone_number", "country", "is_staff")
    list_filter = ("country", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "phone_number")
    list_display_links = ("username",)
    ordering = ("username",)

    # Группировка полей при редактировании пользователя в админке
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "avatar",
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "country",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Поля при создании нового пользователя через админку
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительная информация", {"fields": ("email", "phone_number", "country")}),
    )
