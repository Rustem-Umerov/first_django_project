from typing import Protocol

from .models import Profile


class UserWithProfile(Protocol):
    """
    Класс-Protocol описывает объект у которого есть поле profile, а значение поля объект модели Profile.
    """

    profile: Profile
