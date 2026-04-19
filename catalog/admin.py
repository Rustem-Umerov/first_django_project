from django.contrib import admin

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


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("id", "name", "phone", "email")
    search_fields = ("name", "phone", "email", "address")
    list_display_links = ("name",)
