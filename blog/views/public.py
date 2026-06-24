from django.db.models import Q, QuerySet
from django.views.generic import DetailView, ListView

from ..models import BlogPost


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
