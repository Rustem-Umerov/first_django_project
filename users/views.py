from django.contrib.auth.views import LoginView

from .forms import UserLoginForm


class CustomLoginView(LoginView):
    """Контролер для пользовательского входа."""

    template_name = "users/login.html"
    form_class = UserLoginForm
