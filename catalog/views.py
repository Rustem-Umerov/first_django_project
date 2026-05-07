from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
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
    context = {"products": products}
    return render(request=request, template_name="catalog/home.html", context=context)


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


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Отображает страницу с подробной информацией о товаре.

    :param request: Объект HTTP-запроса.
    :param pk: Ключ к объекту
    :return: Ответ с отрендеренным шаблоном product_detail.html.
    """

    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}

    return render(
        request=request, template_name="catalog/product_detail.html", context=context
    )


def product_create(request: HttpRequest) -> HttpResponse:
    """
    Страница с формой добавления нового продукта.
    При GET показывает пустую форму.
    При POST обрабатывает данные, создаёт продукт и перенаправляет на его страницу.
    """

    if request.method == "GET":
        form = ProductForm()
        context: dict[str, Any] = {"form": form}
        return render(
            request=request,
            template_name="catalog/product_create.html",
            context=context,
        )

    elif request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            product: Product = form.save(commit=False)

            # Забираем файл из cleaned_data
            image = form.cleaned_data.get("image")

            # Временно убираем файл с объекта
            product.image = None

            # Сохраняем объект → появляется pk
            product.save()

            # Если файл был — присваиваем и сохраняем ещё раз
            if image:
                product.image = image
                product.save()

            return redirect(to="catalog:product_detail", pk=product.pk)

        context = {"form": form}
        return render(
            request=request,
            template_name="catalog/product_create.html",
            context=context,
        )

    return HttpResponse(status=405)
