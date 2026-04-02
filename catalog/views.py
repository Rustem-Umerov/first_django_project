from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """
    Отображает главную страницу приложения 'catalog'.

    :param request: Объект HTTP-запроса.
    :return: Ответ с отрендеренным шаблоном home.html.
    """

    return render(request=request, template_name="catalog/home.html")


def contacts(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу с контактной информацией и POST‑форму.

    :param request: Объект HTTP-запроса.
    :return: Ответ с отрендеренным шаблоном contacts.html.
    """

    context = {}

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
