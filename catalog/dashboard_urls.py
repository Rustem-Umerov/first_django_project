from django.urls import path

from .views import (
    DashboardProductCreateView,
    DashboardProductDeleteView,
    DashboardProductDetailView,
    DashboardProductsListView,
    DashboardProductUpdateView,
    DashboardView,
    ReturnProductToDraftView,
    SubmitProductForModerationView,
)

app_name = "catalog_dashboard"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path(
        "products_list/",
        DashboardProductsListView.as_view(),
        name="dashboard_products_list",
    ),
    path(
        "<int:pk>/",
        DashboardProductDetailView.as_view(),
        name="dashboard_product_detail",
    ),
    path(
        "product/create/",
        DashboardProductCreateView.as_view(),
        name="dashboard_product_create",
    ),
    path(
        "products/<int:pk>/edit/",
        DashboardProductUpdateView.as_view(),
        name="dashboard_product_edit",
    ),
    path(
        "products/<int:pk>/delete/",
        DashboardProductDeleteView.as_view(),
        name="dashboard_product_delete",
    ),
    path(
        "products/<int:pk>/return-to-draft/",
        ReturnProductToDraftView.as_view(),
        name="return_product_to_draft",
    ),
    path(
        "products/<int:pk>/for-moderation/",
        SubmitProductForModerationView.as_view(),
        name="submit_product_for_moderation",
    ),
]
