from django.urls import path

from .views import ContactsViews, HomeListViews, ProductDetailView

app_name = "catalog_public"

urlpatterns = [
    path("", HomeListViews.as_view(), name="home"),
    path("contacts/", ContactsViews.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
