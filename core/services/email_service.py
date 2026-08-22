from typing import Any, Optional

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config import settings


class EmailService:
    """
    Универсальный сервис для отправки email‑писем.
    Работает на основе Django EmailMultiAlternatives.
    Поддерживает текстовые и HTML‑шаблоны, вложения и reply_to.
    """

    def __init__(self) -> None:
        """Загружает настройки из settings.py"""
        # Сейчас данные настройки не используются напрямую в методах класса, но оставлены для будущего расширения.

        self.host = settings.EMAIL_HOST
        self.port = settings.EMAIL_PORT
        self.user = settings.EMAIL_HOST_USER
        self.password = settings.EMAIL_HOST_PASSWORD
        self.use_ssl = getattr(settings, "EMAIL_USE_SSL", False)
        self.use_tls = getattr(settings, "EMAIL_USE_TLS", False)

    def send(
        self,
        to_email: str | list[str],
        subject: str,
        template_html: str,
        template_txt: str,
        context: Optional[dict[str, Any]] = None,
        attachments: Optional[list[tuple[str, bytes, str]]] = None,
        reply_to: Optional[str | list[str]] = None,
    ) -> int:
        """
        Метод для отправки email письма на основе EmailMultiAlternatives.
        Рендерит шаблоны (текстовый и html).
        Создает объект письма (EmailMultiAlternatives).
        Добавляет html-версию письма.
        Добавляет вложения, если они есть.
        Отправляет письмо.

        :param to_email: Куда отправить
        :param subject: Заголовок
        :param template_html: Html-шаблон
        :param template_txt: Текст письма
        :param context: Данные для html-шаблона
        :param attachments: Вложения
        :param reply_to: Куда принимать ответ
        :return: Количество адресов на какие было отправлено сообщение / Если была ошибка, то выбрасывает исключение
        """

        try:
            # Рендеринг шаблонов
            text_context = render_to_string(template_txt, context or {})
            html_context = render_to_string(template_html, context or {})

            to_email_list = [to_email] if isinstance(to_email, str) else to_email
            reply_to_list = [reply_to] if isinstance(reply_to, str) else reply_to

            # Создание письма
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_context,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=to_email_list,
                reply_to=reply_to_list,
            )

            # HTML-версия
            email.attach_alternative(html_context, "text/html")

            # Вложения
            if attachments:
                for name, content, mime in attachments:
                    email.attach(name, content, mime)

            # Отправка письма
            sent_count = email.send()
            return sent_count

        except Exception as e:
            raise Exception(f"Ошибка отправки письма: {e}") from e
