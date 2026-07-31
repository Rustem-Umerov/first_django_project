from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View

from ..forms import BlogPostForm
from ..models import BlogPost


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):  # type: ignore[type-arg]
    """Страница для редактирования поста"""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/account/post_form.html"

    def get_queryset(self) -> QuerySet[BlogPost]:
        """Возвращает queryset объектов определенного автора."""

        user = cast(User, self.request.user)
        return BlogPost.objects.filter(author=user)

    def get_success_url(self) -> str:
        """Куда перенаправлять после успешного редактирования."""

        return reverse_lazy(
            "blog_account:my_post_detail", kwargs={"pk": self.object.pk}
        )  # type: ignore[return-value]


class ChangeStatusView(LoginRequiredMixin, View):
    """Меняет статус публикации поста: publish / draft."""

    def get_queryset(self) -> QuerySet[BlogPost]:
        """Разрешаем работать только со своими постами."""

        user = cast(User, self.request.user)
        return BlogPost.objects.filter(author=user)

    def post(self, request: HttpRequest, pk: int, action: str) -> HttpResponse:
        """Обрабатывает нажатие кнопок 'Опубликовать' или 'Перенести в черновик'."""

        # Получаем пост из ограниченного queryset
        post = get_object_or_404(self.get_queryset(), pk=pk)

        new_status = action == "publish"

        if post.is_published != new_status:
            post.is_published = new_status
            post.save()

        redirect_url = (
            "blog_account:my_published" if new_status else "blog_account:my_drafts"
        )
        return redirect(redirect_url)
