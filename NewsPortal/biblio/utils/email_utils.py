from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_new_post_notification(post, subscribers):
    """
    Отправляет уведомление о новом посте подписчикам

    :param post: Объект поста
    :param subscribers: QuerySet подписчиков (объекты CategorySubscriber)
    """
    category = post.categories.first()  # Получаем первую категорию

    for subscriber in subscribers:
        html_content = render_to_string(
            'email/new_post_notification.html',
            {
                'post': post,
                'category': category,
                'site_url': settings.SITE_URL,
                'subscriber': subscriber,  # Теперь subscriber определен
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Новая публикация в категории "{category.name}"' if category else f'Новая публикация: {post.title}',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.user.email],  # Отправляем каждому подписчику отдельно
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()