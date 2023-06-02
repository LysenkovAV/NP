from celery import shared_task
import time
import datetime

from django.conf import settings

from news.models import Post, Category

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Отправка рассылки с постами за неделю
@shared_task
def mail_for_subscribers():
    # определение множества категорий, в которых появились посты за последнюю неделю
    # и определение множества пользователей, который подписаны на эти категории
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_add__gte=last_week)
    categories = set(posts.values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'weekly_posts.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Posts for the week',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
