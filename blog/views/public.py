from typing import Optional

from django.db.models import Q, QuerySet
from django.utils import timezone
from django.views.generic import DetailView, ListView

from ..models import BlogPost, PostView


class BlogPostListView(ListView):  # type: ignore[type-arg]
    """Страница со списком опубликованных постов"""

    model = BlogPost
    template_name = "blog/public/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[BlogPost]:
        """Переопредели get_queryset, чтобы показывать только опубликованные посты."""

        qs = BlogPost.objects.filter(is_published=True)

        # Поиск
        q = self.request.GET.get("q")
        if q and q.strip():
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))

        # Сортировка
        sort = self.request.GET.get("sort")
        if sort:
            if sort == "new":
                qs = qs.order_by("-created_at")
            elif sort == "old":
                qs = qs.order_by("created_at")

        return qs


class BlogPostDetailView(DetailView):  # type: ignore[type-arg]
    """Страница с подробной информацией о посте"""

    model = BlogPost
    template_name = "blog/public/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset: Optional[QuerySet[BlogPost]] = None) -> BlogPost:
        """
        Переопределен метод.
        Добавлена история просмотра для пользователя (авторизованного/неавторизованного)
        Если пользователь авторизован, то мы работаем с базой данных PostView
        Если не авторизован - работаем с сессией.
        """

        post: BlogPost = super().get_object()
        user = self.request.user

        # --- Авторизованный пользователь ---
        # Если пользователь авторизован, то мы работаем с моделью PostView
        if user.is_authenticated:
            # Проверяем смотрел ли данный пост текущий пользователь
            post_view = PostView.objects.filter(post=post, user=user)
            if post_view.exists():
                # Если есть совпадения, то, просто, обновляем дату просмотра
                post_view.update(viewed_at=timezone.now())

            else:
                # Если совпадений нет, создаем запись в базе PostView
                PostView.objects.create(post=post, user=user)
                post.count_views += 1  # Увеличиваем счетчик у поста (объект BlogPost)
                post.save()  # Сохраняем

        # --- Неавторизованный пользователь ---
        else:
            # Получаем объект сессии текущего пользователя
            viewed_posts = self.request.session.get("viewed_posts", [])

            # Если гость ещё не смотрел этот пост, добавляем его pk в список
            if post.pk not in viewed_posts:
                viewed_posts.append(post.pk)
                self.request.session["viewed_posts"] = viewed_posts

                post.count_views += 1  # Увеличиваем счетчик у поста (объект BlogPost)
                post.save()  # Сохраняем

        return post  # Возвращаем объект поста
