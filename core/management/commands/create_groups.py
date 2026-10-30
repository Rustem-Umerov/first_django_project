from typing import Any, Type, cast

from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Model

GROUPS_MODELS_PERMISSIONS = {
    "Модератор продуктов": {
        "catalog.Product": ("can_unpublish_product", "delete_product"),
    },
}


class Command(BaseCommand):
    help = "Инициализирует системные группы пользователей и назначает им права доступа."

    def handle(self, *args: Any, **options: Any) -> None:
        """Запуск логики создания системных групп и привязки прав доступа."""

        # Берем все приложения из settings.INSTALLED_APPS и принудительно генерируем
        # в базе данных все стандартные права (add, change, delete, view)
        # и кастомные права, которые мы прописали в Meta классах наших моделей.
        for app_config in apps.get_app_configs():
            create_permissions(app_config, apps=apps, verbosity=0)

        success_messages_list = []  # Список для накопления сообщений об успехе

        try:
            with transaction.atomic():
                for (
                    group_name,
                    model_and_permissions_codename,
                ) in GROUPS_MODELS_PERMISSIONS.items():

                    # 1. Безопасно создаем или получаем группу
                    group_obj, created = Group.objects.get_or_create(name=group_name)

                    permissions_list = []  # список прав для каждой группы
                    action_word = "Создана" if created else "Обновлена"

                    # 2. Собираем права по всем моделям для этой группы
                    for (
                        model_string,
                        permissions_codename,
                    ) in model_and_permissions_codename.items():

                        # Защита от случайной передачи строки вместо кортежа/списка
                        codenames = (
                            [permissions_codename]
                            if isinstance(permissions_codename, str)
                            else permissions_codename
                        )

                        try:
                            raw_model = apps.get_model(model_string)
                            model_class = cast(Type[Model], raw_model)
                        except (LookupError, ValueError) as e:
                            raise CommandError(
                                f"Критическая ошибка конфигурации! Модель '{model_string}' недоступна: {e}. "
                                f"Убедитесь в правильности формата 'app_label.ModelName' и примените миграции."
                            )

                        content_type = ContentType.objects.get_for_model(model_class)

                        for codename in codenames:
                            try:
                                # Ищем право в базе данных
                                permission_obj = Permission.objects.get(
                                    codename=codename, content_type=content_type
                                )
                                permissions_list.append(permission_obj)
                            except Permission.DoesNotExist:
                                # Если права нет в БД (забыли миграции) пробрасываем ошибку
                                raise CommandError(
                                    f"Критическая ошибка! Право '{codename}' для "
                                    f"модели {model_class.__name__} не найдено в БД. "
                                    f"Сначала запустите миграции, чтобы Django сгенерировал дефолтные права."
                                )

                    # 3. Перезаписываем права для группы (старые стираются, новые пишутся)
                    group_obj.permissions.set(permissions_list)

                    # Добавляем в список сообщение об успехе
                    success_messages_list.append(
                        f"[OK] {action_word} группа '{group_name}'. Привязано прав: {len(permissions_list)}."
                    )

                # После обработки всех групп и их разрешений, вывод сообщений с информацией про каждую группу.
                for message in success_messages_list:
                    self.stdout.write(self.style.SUCCESS(message))

        except Exception as e:
            raise CommandError(
                f"Произошел сбой при обновлении групп: {e}\n"
                f"Все изменения были откатаны. База данных НЕ изменена."
            )
