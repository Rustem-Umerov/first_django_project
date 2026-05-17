from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View

from .forms import ProductForm
from .models import Contact, Product

PER_PAGE = 12


# **** Данная функция нужна была для первых заданий. Сейчас не используется.
# def get_last_products(count: int) -> list[Product]:
#     """
#     Возвращает последние count продуктов, отсортированные по дате создания.
#
#     :param count: Количество элементов
#     :return: Список объектов Product
#     """
#
#     return list(Product.objects.order_by("-created_at")[:count])


# **** Данная функция нужна была для первых заданий. Сейчас не используется.
# def print_products(products: list[Product]) -> None:
#     """
#     Выводит информацию о продуктах в консоль сервера.
#
#     :param products: Список объектов Product
#     """
#
#     for prod in products:
#         print(
#             f"Название продукта: {prod.name}, "
#             f"Цена: {prod.price}, "
#             f"Категория: {prod.category}, "
#             f"Дата создания: {prod.created_at}"
#         )


# # Функциональный контролер главной страницы (FBV)
# def home(request: HttpRequest) -> HttpResponse:
#     """
#     Отображает главную страницу приложения 'catalog'.
#
#     :param request: Объект HTTP-запроса.
#     :return: Ответ с отрендеренным шаблоном home.html.
#     """
#
#     # Получение QuerySet
#     qs_products = Product.objects.all()
#
#     # Создаем объект Paginator
#     paginator = Paginator(qs_products, PER_PAGE)
#
#     # Получение номера страницы из запроса
#     page_number = request.GET.get("page", 1)
#
#     # Попытка получить объекты для одной страницы
#     try:
#         page_obj = paginator.page(page_number)
#
#     except PageNotAnInteger:
#         # если не число — первая страница
#         page_obj = paginator.page(1)
#
#     except EmptyPage:
#         # приводим к int, потому что page_number — строка
#         num = int(page_number)
#
#         if num < 1:
#             # если меньше 1, то первая страницы
#             page_obj = paginator.page(1)
#         else:
#             # если слишком большой номер — последняя страница
#             page_obj = paginator.page(paginator.num_pages)
#
#     # Формирование диапазона страниц, для навигации
#     current_page = page_obj.number
#     total_page = paginator.num_pages
#
#     start_page = max(current_page - 5, 1)
#     end_page = min(current_page + 5, total_page)
#
#     page_range = range(start_page, end_page + 1)
#
#     context = {
#         "page_obj": page_obj,
#         "paginator": paginator,
#         "page_range": page_range,
#     }
#
#     return render(request=request, template_name="catalog/home.html", context=context)


# Классовый контролер для главной страницы
class HomeListViews(ListView):
    """Главная страница каталога с пагинацией."""

    model = Product
    template_name = "catalog/home.html"
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


# # Функциональный контролер для страницы контактов (FBV)
# def contacts(request: HttpRequest) -> HttpResponse:
#     """
#     Отображает страницу с контактной информацией и POST‑форму.
#
#     :param request: Объект HTTP-запроса.
#     :return: Ответ с отрендеренным шаблоном contacts.html.
#     """
#
#     context: dict[str, Any] = {
#         "contacts": Contact.objects.all(),
#     }
#
#     if request.method == "POST":
#         name = request.POST.get("name", "").strip()
#         phone = request.POST.get("phone", "").strip()
#         message = request.POST.get("message", "").strip()
#
#         if not name or not phone or not message:
#             context["error_message"] = "Ошибка: заполните все поля"
#         else:
#             context["success_message"] = "Ваше сообщение успешно отправлено"
#
#     return render(
#         request=request, template_name="catalog/contacts.html", context=context
#     )


# Классовый контролер для страницы контактов
class ContactsViews(View):
    """Контроллер страницы контактов."""

    model = Contact
    template_name = "catalog/contacts.html"

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


# # Функциональный контролер для страницы с подробной информацией о товаре (FBV)
# def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
#     """
#     Отображает страницу с подробной информацией о товаре.
#
#     :param request: Объект HTTP-запроса.
#     :param pk: Ключ к объекту
#     :return: Ответ с отрендеренным шаблоном product_detail.html.
#     """
#
#     product = get_object_or_404(Product, pk=pk)
#     context = {"product": product}
#
#     return render(
#         request=request, template_name="catalog/product_detail.html", context=context
#     )


# Классовый контролер для страницы с подробной информацией о товаре
class ProductDetailView(DetailView):
    """Страница с подробной информацией о товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


# # Функциональный контролер для страницы с формой добавления нового продукта (FBV)
# def product_create(request: HttpRequest) -> HttpResponse:
#     """
#     Страница с формой добавления нового продукта.
#     При GET показывает пустую форму.
#     При POST обрабатывает данные, создаёт продукт и перенаправляет на его страницу.
#     """
#
#     if request.method == "GET":
#         form = ProductForm()
#         context: dict[str, Any] = {"form": form}
#         return render(
#             request=request,
#             template_name="catalog/product_create.html",
#             context=context,
#         )
#
#     elif request.method == "POST":
#         form = ProductForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#
#             # Создаём объект без сохранения
#             product: Product = form.save(commit=False)
#
#             # Забираем файл из cleaned_data
#             image = form.cleaned_data.get("image")
#
#             # Временно убираем файл с объекта
#             product.image = None
#
#             # Сохраняем объект → появляется pk
#             product.save()
#
#             # Если файл был — присваиваем и сохраняем ещё раз
#             if image:
#                 product.image = image
#                 product.save()
#
#             return redirect(to="catalog:product_detail", pk=product.pk)
#
#         context = {"form": form}
#         return render(
#             request=request,
#             template_name="catalog/product_create.html",
#             context=context,
#         )
#
#     return HttpResponse(status=405)


# Классовый контролер для страницы создания нового продукта
class ProductCreateView(CreateView):
    """Страница создания нового продукта."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_create.html"

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

        # Передаём управление родителю (он сделает redirect)
        return super().form_valid(form=form)

    def get_success_url(self):
        """Куда перенаправлять после успешного создания."""

        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})
