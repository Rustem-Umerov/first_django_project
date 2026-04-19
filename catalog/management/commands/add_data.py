from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add test data to the database"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        """
        Основной метод кастомной команды.
        Предварительно очищает базу данных.
        Загружает тестовые данные из фикстуры в базу данных.
        """

        # 1. Удаляем продукты
        deleted_products, _ = Product.objects.all().delete()
        self.stdout.write(self.style.WARNING(f"Удалено продуктов: {deleted_products}"))

        # 2. Удаляем категории
        deleted_categories, _ = Category.objects.all().delete()
        self.stdout.write(
            self.style.WARNING(f"Удалено категорий: {deleted_categories}")
        )

        # 3. Загружаем фикстуру
        self.stdout.write("Загружаю фикстуру add_data.json...")
        call_command("loaddata", "catalog/fixtures/data.json")

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены"))
