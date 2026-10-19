from __future__ import annotations

from typing import Any

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import UserLoginForm, UserProfileUpdateForm, UserRegisterForm


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


class UserRegisterView(CreateView):  # type: ignore[type-arg]
    """Контролер для создания пользователя."""

    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        """Автоматически авторизует пользователя после успешной регистрации."""

        # Сначала сохраняем пользователя в базу
        # и передаем в response объект HttpResponseRedirect на success_url (здесь же сработает сигнал отправки почты)
        response = super().form_valid(form)

        # Авторизуем пользователя в текущей сессии
        login(self.request, self.object)

        # Возвращаем объект редиректа на success_url
        return response


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):  # type: ignore[type-arg]
    """Контроллер для просмотра и обновления профиля пользователя."""

    form_class = UserProfileUpdateForm
    template_name = "users/profile.html"

    def get_object(self, queryset: Any = None) -> Any:
        """Возвращает текущего авторизованного пользователя."""

        return self.request.user

    def get_success_url(self) -> str:
        """Возвращает URL текущей страницы для перезагрузки после сохранения."""

        return self.request.path
