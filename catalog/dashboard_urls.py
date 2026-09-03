from django.urls import path

from .views import (
    AccountDashboardView,
    DashboardProductDetailView,
    DashboardProductsListView,
    ProductCreateView,
)

app_name = "catalog_dashboard"

urlpatterns = [
    path("dashboard/", AccountDashboardView.as_view(), name="dashboard"),
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
        "product/create/", ProductCreateView.as_view(), name="dashboard_product_create"
    ),
    # path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="dashboard_product_edit"),
    # path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="dashboard_product_delete"),
]
