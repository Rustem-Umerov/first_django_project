from django.urls import path

from catalog.apps import CatalogConfig

from .views import ContactsViews, HomeListViews, ProductCreateView, ProductDetailView

# from catalog.views import product_create, product_detail, contacts, home

app_name = CatalogConfig.name

urlpatterns = [
    # path("", home, name="home"),  # путь для функционального контролера
    path("", HomeListViews.as_view(), name="home"),  # путь для классового контролера
    # path("contacts/", contacts, name="contacts"),  # путь для функционального контролера
    path(
        "contacts/", ContactsViews.as_view(), name="contacts"
    ),  # путь для классового контролера
    # path("products/<int:pk>/", product_detail, name="product_detail"),  # путь для функционального контролера
    path(
        "products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"
    ),  # путь для классового контролера
    # path("products/create/", product_create, name="product_create"),  # путь для функционального контролера
    path(
        "products/create/", ProductCreateView.as_view(), name="product_create"
    ),  # путь для классового контролера
]
