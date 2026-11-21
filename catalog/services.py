from django.db.models import Q, QuerySet

from users.models import CustomUser

from .models import Product


def get_accessible_products(
    *, user: CustomUser, queryset: QuerySet[Product], permission: str
) -> QuerySet[Product]:
    """Возвращает QuerySet продуктов, доступных пользователю."""

    if not user.has_perm(permission):
        return queryset.filter(author=user)

    return queryset.exclude(Q(status=Product.Status.DRAFT) & ~Q(author=user))
