from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import BlogPost, Profile
from .typing import UserWithProfile


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("author", "title", "is_published", "created_at", "count_views")
    list_filter = ("author", "is_published", "created_at")
    search_fields = ("title", "content")
    ordering = ("-created_at",)


# ==================================================================
# ========== Интегрируем модель Profile в класс UserAdmin ==========


class ProfileInline(admin.StackedInline):  # type: ignore[type-arg]
    model = Profile
    exclude = ("user",)
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
