from django.urls import path

from .views.public import BlogPostDetailView, BlogPostListView

app_name = "blog_public"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="post_list"),
    path("<int:pk>/", BlogPostDetailView.as_view(), name="post_detail"),
]
