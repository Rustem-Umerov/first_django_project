from django.db.models import Q, QuerySet

from users.models import CustomUser

from .models import BlogPost


def get_accessible_blog_posts(
    *, user: CustomUser, queryset: QuerySet[BlogPost], permission: str
) -> QuerySet[BlogPost]:
    """Возвращает QuerySet постов, доступных пользователю."""

    # Суперпользователь видит абсолютно все посты.
    if user.is_superuser:
        return queryset

    # Если нет права, то только собственные посты.
    if not user.has_perm(permission):
        return queryset.filter(author=user)

    # Контент-менеджер видит все посты, кроме чужих черновиков.
    return queryset.exclude(Q(is_published=False) & ~Q(author=user))
