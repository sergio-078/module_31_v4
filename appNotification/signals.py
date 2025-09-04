from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from .models import News, Subscription

def get_user_action_log_model():
    return apps.get_model('appUser', 'UserActionLog')


@receiver(post_save, sender='appNotification.Response')
def notify_post_author_on_response(sender, instance, created, **kwargs):
    if created:
        UserActionLog = get_user_action_log_model()

        subject = _('New response to your post')
        message = render_to_string('appNotification/emails/response_created.txt', {
            'post': instance.post,
            'response': instance,
            'SITE_URL': settings.SITE_URL  # Добавляем SITE_URL в контекст
        })

        # Для разработки
        print(f"\n=== NEW RESPONSE NOTIFICATION ===")
        print(f"To: {instance.post.author.email}")
        print(f"Subject: {subject}")
        print(f"Post: {instance.post.title}")
        print(f"From: {instance.author.email}")
        print(f"Link: {settings.SITE_URL}{instance.post.get_absolute_url()}")
        print("===============================\n")

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.post.author.email],
            fail_silently=False,
        )

        UserActionLog.objects.create(
            user=instance.author,
            action=f"Created response to post {instance.post.id}",
        )


@receiver(post_save, sender='appNotification.Response')
def notify_response_author_on_accept(sender, instance, **kwargs):
    if instance.is_accepted:
        UserActionLog = get_user_action_log_model()

        subject = _('Your response was accepted')
        message = render_to_string('appNotification/emails/response_accepted.txt', {
            'post': instance.post,
            'response': instance,
            'SITE_URL': settings.SITE_URL  # Добавляем SITE_URL в контекст
        })

        # Для разработки
        print(f"\n=== RESPONSE ACCEPTED NOTIFICATION ===")
        print(f"To: {instance.author.email}")
        print(f"Subject: {subject}")
        print(f"Post: {instance.post.title}")
        print(f"Link: {settings.SITE_URL}{instance.post.get_absolute_url()}")
        print("====================================\n")

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.author.email],
            fail_silently=False,
        )

        UserActionLog.objects.create(
            user=instance.post.author,
            action=f"Accepted response {instance.id} to post {instance.post.id}",
        )


@receiver(post_save, sender=News)
def notify_subscribers_on_new_news(sender, instance, created, **kwargs):
    """
    Отправляет уведомления подписчикам при создании новой новости
    """
    if created and instance.notify_subscribers:
        from appUser.models import UserActionLog

        # Получаем всех подписчиков на новости
        news_subscribers = Subscription.objects.filter(news=True).select_related('user')

        if news_subscribers.exists():
            subject = _('New news on MMORPG Portal: {}').format(instance.title)

            for subscription in news_subscribers:
                message = render_to_string('appNotification/emails/new_news_notification.txt', {
                    'news': instance,
                    'user': subscription.user,
                    'SITE_URL': settings.SITE_URL
                })

                # Для разработки
                print(f"\n=== NEW NEWS NOTIFICATION ===")
                print(f"To: {subscription.user.email}")
                print(f"Subject: {subject}")
                print(f"News: {instance.title}")
                print(f"Link: {settings.SITE_URL}{instance.get_absolute_url()}")
                print("=============================\n")

                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [subscription.user.email],
                        fail_silently=False,
                    )

                    UserActionLog.objects.create(
                        user=subscription.user,
                        action=f"Received notification about news {instance.id}",
                    )
                except Exception as e:
                    print(f"Error sending news notification to {subscription.user.email}: {e}")
