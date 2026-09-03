from django.urls import path

from .views.account import (
    AccountDashboardView,
    BlogPostCreateView,
    BlogPostDeleteView,
    BlogPostDraftListView,
    BlogPostMyDetailView,
    BlogPostMyPublishedListView,
)
from .views.posts import BlogPostUpdateView, ChangeStatusView

app_name = "blog_account"

urlpatterns = [
    path("dashboard/", AccountDashboardView.as_view(), name="dashboard"),
    path("published/", BlogPostMyPublishedListView.as_view(), name="my_published"),
    path("drafts/", BlogPostDraftListView.as_view(), name="my_drafts"),
    path("create/", BlogPostCreateView.as_view(), name="my_post_create"),
    path("<int:pk>/", BlogPostMyDetailView.as_view(), name="my_post_detail"),
    path("<int:pk>/edit/", BlogPostUpdateView.as_view(), name="my_post_edit"),
    path("<int:pk>/delete/", BlogPostDeleteView.as_view(), name="my_post_delete"),
    path(
        "post/<int:pk>/<str:action>/",
        ChangeStatusView.as_view(),
        name="my_post_change_status",
    ),
]
