from django.db import models


class Category(models.Model):
    """
    Модель категории продуктов.
    Хранит информацию о названии категории о ее описание.
    """

    name = models.CharField(
        max_length=150, verbose_name="Название категории", unique=True
    )
    description = models.TextField(verbose_name="Описание категории", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """
    Модель продукта.
    Хранит информацию о товаре, его категории, цене и датах создания/обновления.
    """

    name = models.CharField(max_length=150, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание продукта")

    def get_image_path(self, filename: str) -> str:
        """
        Формирует путь к месту хранения файла для модели Product

        :param filename: Название файл
        :return: Путь к месту хранения файла
        """

        return f"catalog/products/{self.pk}/{filename}"

    image = models.ImageField(
        upload_to=get_image_path,
        verbose_name="Фото продукта",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"], name="unique_product_in_category"
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} — {self.price} ₽"


class Contact(models.Model):
    """
    Модель для хранения контактных данных
    """

    name = models.CharField(
        max_length=150,
        verbose_name="Название",
        help_text="Например: Главный офис, Техподдержка, Менеджер",
    )
    phone = models.CharField(max_length=20, verbose_name="Телефон", unique=True)
    email = models.EmailField(
        verbose_name="Email", help_text="Рабочий email для связи", unique=True
    )
    address = models.TextField(
        verbose_name="Адрес",
        help_text="Фактический адрес офиса (необязательно)",
        blank=True,
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} — {self.phone}"
