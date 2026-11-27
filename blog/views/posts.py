from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View

from users.models import CustomUser

from ..forms import BlogPostForm
from ..models import BlogPost
from ..services import get_accessible_blog_posts


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):  # type: ignore[type-arg]
    """Страница для редактирования поста"""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/account/post_form.html"

    def get_queryset(self) -> QuerySet[BlogPost]:
        """Возвращает посты, доступные пользователю для редактирования."""

        user = cast(CustomUser, self.request.user)
        queryset = super().get_queryset()

        return get_accessible_blog_posts(
            user=user, queryset=queryset, permission="blog.change_blogpost"
        )

    def get_success_url(self) -> str:
        """Куда перенаправлять после успешного редактирования."""

        return reverse_lazy(
            "blog_account:my_post_detail", kwargs={"pk": self.object.pk}
        )  # type: ignore[return-value]


class ChangeStatusView(LoginRequiredMixin, View):
    """Меняет статус публикации поста: publish / draft."""

    def post(self, request: HttpRequest, pk: int, action: str) -> HttpResponse:
        """Обрабатывает нажатие кнопок 'Опубликовать' или 'Перенести в черновик'."""

        user = cast(CustomUser, self.request.user)

        # Суперпользователь может менять статус любых постов.
        if user.is_superuser:
            queryset = BlogPost.objects.all()
        else:
            # Остальные пользователи могут менять статус только своих постов.
            queryset = BlogPost.objects.filter(author=user)

        post = get_object_or_404(queryset, pk=pk)

        new_status = action == "publish"

        if post.is_published != new_status:
            post.is_published = new_status
            post.save(update_fields=["is_published"])

        redirect_url = (
            "blog_account:my_published" if new_status else "blog_account:my_drafts"
        )
        return redirect(redirect_url)
