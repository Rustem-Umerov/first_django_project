from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class UserLoginForm(AuthenticationForm):
    """
    Форма для авторизации пользователя по электронной почте и паролю.
    В форме переопределено поле username.
    """

    username = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={"placeholder": "E-mail", "autofocus": True}),
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # Проходим циклом по всем полям и добавляем им класс Bootstrap
        for field_name, field_object in self.fields.items():
            field_object.widget.attrs.update({"class": "form-control"})


class UserRegisterForm(UserCreationForm[CustomUser]):
    """Форма регистрации нового пользователя."""

    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # Проходим циклом по всем полям и добавляем им класс Bootstrap
        for field_name, field_object in self.fields.items():
            field_object.widget.attrs.update({"class": "form-control"})


class UserProfileUpdateForm(forms.ModelForm[CustomUser]):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        model = CustomUser
        fields = (
            "avatar",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "country",
        )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # Проходим циклом по всем полям и добавляем им класс Bootstrap
        for field_name, field_object in self.fields.items():
            field_object.widget.attrs.update({"class": "form-control"})
