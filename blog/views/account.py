from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
)

from ..forms import BlogPostForm
from ..models import BlogPost


class AccountDashboardView(LoginRequiredMixin, TemplateView):
    """Главная страница аккаунта"""

    template_name = "blog/account/dashboard.html"


class BlogPostMyPublishedListView(LoginRequiredMixin, ListView):  # type: ignore[type-arg]
    """Страница с личными опубликованными постами"""

    model = BlogPost
    template_name = "blog/account/my_published.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[BlogPost]:
        """Переопредели get_queryset, чтобы показывать только личные опубликованные посты."""

        user = cast(User, self.request.user)
        return BlogPost.objects.filter(is_published=True, author=user)


class BlogPostDraftListView(LoginRequiredMixin, ListView):  # type: ignore[type-arg]
    """Страница-черновик с личными постами (не опубликованные посты)"""

    model = BlogPost
    template_name = "blog/account/my_drafts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[BlogPost]:
        """Переопредели get_queryset, чтобы показывать только личные не опубликованные посты."""

        user = cast(User, self.request.user)
        return BlogPost.objects.filter(is_published=False, author=user)


class BlogPostCreateView(LoginRequiredMixin, CreateView):  # type: ignore[type-arg]
    """Страница для создания поста"""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/account/post_form.html"

    def form_valid(self, form: BlogPostForm) -> HttpResponse:
        """
        Переопределение метода
        создаем объект, но не сохраняем
        назначаем автора
        определяем из запроса статус(is_published) поста
        сохраняем объект
        вызываем родительский метод
        """

        # Создаём объект без сохранения
        post = form.save(commit=False)

        # Назначаем автора
        post.author = self.request.user

        # статус публикации
        action = self.request.POST.get("action")
        post.is_published = action == "publish"

        # временно убираем картинку
        post.image = None

        # Сохраняем объект
        post.save()

        # берём картинку из формы
        image = form.cleaned_data.get("image")

        if image:
            post.image = image
            post.save()

        self.object = post  # передаем в object наш объект

        # Вызываем get_success_url
        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        """Куда перенаправлять после успешного создания."""

        assert self.object is not None
        return reverse_lazy(
            "blog_account:my_post_detail", kwargs={"pk": self.object.pk}
        )  # type: ignore[return-value]


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):  # type: ignore[type-arg]
    """Удаление поста"""

    model = BlogPost
    context_object_name = "post"
    # template_name нет, так как подтверждения удаления происходит в окне, а не на отдельной странице

    def get_queryset(self) -> QuerySet[BlogPost]:
        """Возвращает queryset объектов определенного автора."""

        user = cast(User, self.request.user)
        return BlogPost.objects.filter(author=user)

    def get_success_url(self) -> str:
        """Куда перенаправлять после успешного удаления."""

        post = self.object

        if post.is_published:
            return reverse_lazy("blog_account:my_published")  # type: ignore[return-value]
        else:
            return reverse_lazy("blog_account:my_drafts")  # type: ignore[return-value]


class BlogPostMyDetailView(LoginRequiredMixin, DetailView):  # type: ignore[type-arg]
    """Страница с подробной информацией о посте в Личном кабинете"""

    model = BlogPost
    template_name = "blog/account/my_post_detail.html"
    context_object_name = "post"

    def get_queryset(self) -> QuerySet[BlogPost]:
        """Возвращает queryset объектов определенного автора."""

        user = cast(User, self.request.user)
        return BlogPost.objects.filter(author=user)
