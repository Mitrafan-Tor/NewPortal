from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Post
import logging

logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=Post.categories.through)
def notify_about_new_post(sender, instance, action, pk_set, **kwargs):

    if action == "post_add" and pk_set:
        try:
            categories = instance.categories.all()
            if not categories:
                return

            subscribers_emails = set()
            subscribed_users = set()  # Чтобы избежать дублирования

            for category in categories:
                subscribers = CategorySubscriber.objects.filter(category=category).select_related('user')
                for sub in subscribers:
                    if sub.user.email and sub.user not in subscribed_users:
                        subscribers_emails.add(sub.user.email)
                        subscribed_users.add(sub.user)

            if subscribers_emails:
                send_post_notification(instance, categories.first(), subscribers_emails)

        except Exception as e:
            logger.error(f"Ошибка при отправке уведомлений: {str(e)}", exc_info=True)


def send_post_notification(post, category, recipients):
    """
    Отправка email-уведомления о новой публикации
    """
    try:
        subject = f'Новая публикация в категории "{category.name}"'

        html_content = render_to_string(
            'email/new_post_notification.html',
            {
                'post': post,
                'category': category,
                'site_url': settings.SITE_URL
            }
        )

        # Для тестирования - вывод в консоль
        if settings.DEBUG:
            print(f"Отправка письма подписчикам {recipients}")
            print(html_content)
            return

        msg = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            bcc=list(recipients),  # Используем BCC для скрытия списка получателей
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {str(e)}", exc_info=True)