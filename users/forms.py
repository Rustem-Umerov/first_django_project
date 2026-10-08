from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    """
    Форма для авторизации пользователя по электронной почте и паролю.
    В форме переопределено поле username.
    """

    username = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={"placeholder": "E-mail", "autofocus": True}),
    )
