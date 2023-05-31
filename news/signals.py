from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import PostCategory


# Отправка письма пользователям
def send_notification(preview, pk, title, subscribers):
    html_content = render_to_string(
        'mail_post_created.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# Отправка письма пользователям, подписанным на категорию, при появлении нового поста в этой категории (по сигналу)
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()
        subscribers = [subscriber.email for subscriber in subscribers]
        send_notification(instance.preview(), instance.pk, instance.title, subscribers)