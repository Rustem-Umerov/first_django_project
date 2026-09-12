from django.urls import path

from .views import (
    DashboardProductCreateView,
    DashboardProductDeleteView,
    DashboardProductDetailView,
    DashboardProductsListView,
    DashboardProductUpdateView,
    DashboardView,
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
]
