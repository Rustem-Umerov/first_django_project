from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, View

from .forms import ProductForm
from .models import Contact, Product

PER_PAGE = 12


# Классовый контролер для главной страницы
class HomeListViews(ListView):
    """Главная страница каталога с пагинацией."""

    model = Product
    template_name = "catalog/public/home.html"
    context_object_name = "products"
    paginate_by = PER_PAGE

    def get_context_data(self, **kwargs) -> dict:
        """Добавляет кастомный диапазон страниц (page_range) в контекст."""

        context = super().get_context_data(**kwargs)

        # Формирование диапазона страниц, для навигации
        current_page = context["page_obj"].number
        total_page = context["paginator"].num_pages

        start_page = max(current_page - 5, 1)
        end_page = min(current_page + 5, total_page)

        page_range = range(start_page, end_page + 1)

        context["page_range"] = page_range
        return context


# Классовый контролер для страницы контактов
class ContactsViews(View):
    """Контроллер страницы контактов."""

    model = Contact
    template_name = "catalog/public/contacts.html"

    def basic_context(self) -> dict:
        """Базовый контекст, который нужен и для GET, и для POST."""

        return {
            "contacts": self.model.objects.all(),
        }

    def get(self, request: HttpRequest):
        """Обработка GET-запроса: просто показать страницу."""

        context = self.basic_context()
        return render(
            request=request, template_name=self.template_name, context=context
        )

    def post(self, request: HttpRequest):
        """Обработка POST-запроса: обработать форму и показать результат."""

        context = self.basic_context()

        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not phone or not message:
            context["error_message"] = "Ошибка: заполните все поля"
        else:
            context["success_message"] = "Ваше сообщение успешно отправлено"

        return render(
            request=request, template_name=self.template_name, context=context
        )


# Классовый контролер для страницы с подробной информацией о товаре
class ProductDetailView(DetailView):
    """Страница с подробной информацией о продукте."""

    model = Product
    template_name = "catalog/public/product_detail.html"
    context_object_name = "product"


# Классовый контролер для страницы создания нового продукта
class ProductCreateView(CreateView):
    """Страница создания нового продукта."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/dashboard/dashboard_product_create.html"

    def form_valid(self, form: ProductForm):
        """
        Переопределение метода:
        создаем объект, но не сохраняем, так как pk еще нет
        получаем фото, и удаляем его из объекта
        сохраняем объект
        если фото было, то возвращаем его в объект
        сохраняем объект с фото (уже есть pk)
        передаем объект в self.object
        вызываем form_valid из родительского класса
        """

        # Создаём объект без сохранения
        product: Product = form.save(commit=False)

        # Забираем файл из cleaned_data
        image = form.cleaned_data.get("image")

        # Временно убираем файл, чтобы сохранить объект и получить pk
        product.image = None
        product.save()

        # Если файл был — присваиваем и сохраняем ещё раз
        if image:
            product.image = image
            product.save()

        # Сообщаем CreateView, какой объект создан
        self.object = product

        # Вызываем get_success_url
        return redirect(self.get_success_url())

    def get_success_url(self):
        """Куда перенаправлять после успешного создания."""

        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class DashboardProductsListView(ListView):
    """Страница каталога в личном кабинете с пагинацией."""

    model = Product
    template_name = "catalog/dashboard/dashboard_products_list.html"
    context_object_name = "products"
    paginate_by = PER_PAGE

    def get_context_data(self, **kwargs) -> dict:
        """Добавляет кастомный диапазон страниц (page_range) в контекст."""

        context = super().get_context_data(**kwargs)

        # Формирование диапазона страниц, для навигации
        current_page = context["page_obj"].number
        total_page = context["paginator"].num_pages

        start_page = max(current_page - 5, 1)
        end_page = min(current_page + 5, total_page)

        page_range = range(start_page, end_page + 1)

        context["page_range"] = page_range
        return context


class AccountDashboardView(LoginRequiredMixin, TemplateView):
    """Главная страница Личного кабинета"""

    template_name = "catalog/dashboard/dashboard_home.html"


class DashboardProductDetailView(LoginRequiredMixin, DetailView):  # type: ignore[type-arg]
    """Страница с подробной информацией о продукте в Личном кабинете"""

    model = Product
    template_name = "catalog/dashboard/dashboard_product_detail.html"
    context_object_name = "product"
