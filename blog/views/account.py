from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
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

from users.models import CustomUser

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
        """Возвращает опубликованные посты, доступные пользователю."""

        # Получаем все опубликованные посты.
        queryset = BlogPost.objects.filter(is_published=True)

        # Если нет права, то только свои посты.
        if not self.request.user.has_perm("blog.view_blogpost"):
            user = cast(CustomUser, self.request.user)
            queryset = queryset.filter(author=user)

        # Если право есть, то все опубликованные посты. В том числе это и для суперпользователя.
        return queryset


class BlogPostDraftListView(LoginRequiredMixin, ListView):  # type: ignore[type-arg]
    """Страница-черновик с личными постами (не опубликованные посты)"""

    model = BlogPost
    template_name = "blog/account/my_drafts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[BlogPost]:
        """Переопредели get_queryset, чтобы показывать только личные не опубликованные посты."""

        queryset = BlogPost.objects.filter(is_published=False)

        # Если не суперпользователь, то фильтруем еще по авторству.
        # Так как обычный пользователь и контент-менеджер не могут видеть чужие черновики.
        if not self.request.user.is_superuser:
            user = cast(CustomUser, self.request.user)
            queryset = queryset.filter(author=user)

        return queryset


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
        """Возвращает посты, доступные пользователю для удаления."""

        user = cast(CustomUser, self.request.user)
        queryset = super().get_queryset()

        # Суперпользователь может удалять любые посты.
        if user.is_superuser:
            return queryset

        # Контент-менеджер может удалять все опубликованные посты и собственные черновики.
        if user.has_perm("blog.delete_blogpost"):
            return queryset.exclude(Q(is_published=False) & ~Q(author=user))

        # Обычный пользователь может удалять только свои посты.
        return queryset.filter(author=user)

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
        """Возвращает посты, доступные пользователю для просмотра."""

        user = cast(CustomUser, self.request.user)
        queryset = super().get_queryset()

        # Суперпользователь может просматривать любые посты.
        if user.is_superuser:
            return queryset

        # Контент-менеджер может просматривать все опубликованные посты и собственные черновики.
        if user.has_perm("blog.view_blogpost"):
            return queryset.exclude(Q(is_published=False) & ~Q(author=user))

        # Обычный пользователь может просматривать только свои посты.
        return queryset.filter(author=user)
