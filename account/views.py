from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def logout_and_stay(request: HttpRequest) -> HttpResponse:
    """
    Завершает сессию пользователя и возвращает его на страницу,
    с которой был отправлен запрос на выход.

    Поведение:
    - выполняет logout()
    - добавляет сообщение об успешном выходе
    - делает redirect на next_url, если он есть, иначе делает redirect обратно на страницу-источник (HTTP_REFERER)
      или на главную страницу, если источник неизвестен

    :param request: объект HttpRequest текущего пользователя
    :return: HttpResponse с перенаправлением на предыдущую страницу
    """

    logout(request)
    messages.success(request, "Вы вышли из аккаунта")

    next_url = request.GET.get("next")
    if next_url:
        return redirect(next_url)

    return redirect(request.META.get("HTTP_REFERER", "/"))
