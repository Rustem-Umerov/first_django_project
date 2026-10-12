from typing import Any

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse

from .forms import UserLoginForm


class CustomLoginView(LoginView):
    """Контролер для пользовательского входа."""

    template_name = "users/login.html"
    form_class = UserLoginForm


class CustomLogoutView(LogoutView):
    """Контролер для пользовательского выхода из аккаунта."""

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Добавляет сообщение об успешном выходе из аккаунта."""

        messages.success(request, "Вы вышли из аккаунта")

        return super().post(request, *args, **kwargs)

    def get_success_url(self) -> str:
        """
        Делает redirect на next_url, если он есть, иначе делает redirect обратно на страницу-источник (HTTP_REFERER)
        или на главную страницу, если источник неизвестен.
        """

        next_url = self.request.GET.get("next")

        if next_url:
            return next_url

        return self.request.META.get("HTTP_REFERER") or "/"
