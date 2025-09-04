from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_weekly_newsletter():
    """Еженедельная рассылка новостей"""
    from .models import News, Subscription
    from appUser.models import UserActionLog

    try:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        weekly_news = News.objects.filter(created_at__range=(start_date, end_date))

        if weekly_news.exists():
            subscriptions = Subscription.objects.filter(news=True).select_related('user')

            for subscription in subscriptions:
                subject = _('Weekly news digest from our portal')
                message = render_to_string('appNotification/emails/weekly_news.txt', {
                    'news': weekly_news,
                    'user': subscription.user,
                    'start_date': start_date,
                    'end_date': end_date,
                    'SITE_URL': settings.SITE_URL  # Добавляем SITE_URL
                })

                # Для разработки
                print(f"\n=== WEEKLY NEWSLETTER ===")
                print(f"To: {subscription.user.email}")
                print(f"Subject: {subject}")
                print(f"News count: {weekly_news.count()}")
                print("=========================\n")

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [subscription.user.email],
                    fail_silently=False,
                )

                UserActionLog.objects.create(
                    user=subscription.user,
                    action="Received weekly news digest",
                )

        return f'Sent weekly newsletter to {subscriptions.count()} subscribers'

    except Exception as e:
        logger.error(f"Error sending weekly newsletter: {e}")
        return f'Error: {e}'


@shared_task
def send_weekly_posts_digest():
    """Еженедельная рассылка постов по категориям"""
    from .models import Post, Subscription, Category
    from appUser.models import UserActionLog

    try:
        categories = Subscription.objects.exclude(category=None).values_list('category', flat=True).distinct()
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)

        for category_id in categories:
            weekly_posts = Post.objects.filter(
                category_id=category_id,
                created_at__range=(start_date, end_date)
            )

            if weekly_posts.exists():
                subscriptions = Subscription.objects.filter(category_id=category_id).select_related('user')

                for subscription in subscriptions:
                    subject = _('Weekly posts digest in your subscribed category')
                    message = render_to_string('appNotification/emails/weekly_posts.txt', {
                        'posts': weekly_posts,
                        'user': subscription.user,
                        'category': subscription.category,
                        'start_date': start_date,
                        'end_date': end_date,
                        'SITE_URL': settings.SITE_URL  # Добавляем SITE_URL
                    })

                    # Для разработки
                    print(f"\n=== CATEGORY DIGEST ===")
                    print(f"To: {subscription.user.email}")
                    print(f"Category: {subscription.category.name}")
                    print(f"Posts count: {weekly_posts.count()}")
                    print("=======================\n")

                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [subscription.user.email],
                        fail_silently=False,
                    )

                    UserActionLog.objects.create(
                        user=subscription.user,
                        action=f"Received weekly posts digest for category {subscription.category.name}",
                    )

        return 'Weekly posts digest sent successfully'

    except Exception as e:
        logger.error(f"Error sending weekly posts digest: {e}")
        return f'Error: {e}'


@shared_task
def send_news_notification(news_id):
    """Асинхронная отправка уведомлений о новой новости"""
    from .models import News, Subscription
    from appUser.models import UserActionLog

    try:
        news = News.objects.get(id=news_id)
        subscribers = Subscription.objects.filter(news=True).select_related('user')

        for subscription in subscribers:
            subject = _('New news on MMORPG Portal: {}').format(news.title)
            message = render_to_string('appNotification/emails/new_news_notification.txt', {
                'news': news,
                'user': subscription.user,
                'SITE_URL': settings.SITE_URL
            })

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [subscription.user.email],
                fail_silently=False,
            )

            UserActionLog.objects.create(
                user=subscription.user,
                action=f"Received notification about news {news.id}",
            )

        return f'Sent news notification to {subscribers.count()} subscribers'

    except Exception as e:
        logger.error(f"Error sending news notifications: {e}")
        return f'Error: {e}'
