from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Contact, Product


def get_last_products(count: int) -> list[Product]:
    """
    Возвращает последние count продуктов, отсортированные по дате создания.

    :param count: Количество элементов
    :return: Список объектов Product
    """

    return list(Product.objects.order_by("-created_at")[:count])


def print_products(products: list[Product]) -> None:
    """
    Выводит информацию о продуктах в консоль сервера.

    :param products: Список объектов Product
    """

    for prod in products:
        print(
            f"Название продукта: {prod.name}, "
            f"Цена: {prod.price}, "
            f"Категория: {prod.category}, "
            f"Дата создания: {prod.created_at}"
        )


def home(request: HttpRequest) -> HttpResponse:
    """
    Отображает главную страницу приложения 'catalog'.

    :param request: Объект HTTP-запроса.
    :return: Ответ с отрендеренным шаблоном home.html.
    """

    products = get_last_products(5)
    print_products(products)
    return render(request=request, template_name="catalog/home.html")


def contacts(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу с контактной информацией и POST‑форму.

    :param request: Объект HTTP-запроса.
    :return: Ответ с отрендеренным шаблоном contacts.html.
    """

    context: dict[str, Any] = {
        "contacts": Contact.objects.all(),
    }

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not phone or not message:
            context["error_message"] = "Ошибка: заполните все поля"
        else:
            context["success_message"] = "Ваше сообщение успешно отправлено"

    return render(
        request=request, template_name="catalog/contacts.html", context=context
    )
