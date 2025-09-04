from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail
from .models import CustomUser, UserActionLog, EmailVerification


@receiver(post_save, sender=CustomUser)
def log_user_creation(sender, instance, created, **kwargs):
    """
    Создает запись в логе при создании нового пользователя
    """
    if created:
        UserActionLog.objects.create(
            user=instance,
            action="User account created",
            ip_address=None
        )

        # Создаем верификацию и отправляем email
        verification = EmailVerification.create_verification(instance)
        verification.send_verification_email()

        # Для разработки - вывод в консоль
        print(f"\n=== USER CREATED ===")
        print(f"Email: {instance.email}")
        print(f"Active: {instance.is_active}")
        print("===================\n")


@receiver(pre_save, sender=CustomUser)
def log_user_changes(sender, instance, **kwargs):
    """
    Логирует изменения в профиле пользователя
    """
    if instance.pk:
        try:
            old_user = CustomUser.objects.get(pk=instance.pk)
            changes = []

            # Проверяем изменения полей
            if old_user.first_name != instance.first_name:
                changes.append(f"first_name: {old_user.first_name} → {instance.first_name}")

            if old_user.last_name != instance.last_name:
                changes.append(f"last_name: {old_user.last_name} → {instance.last_name}")

            if old_user.email != instance.email:
                changes.append(f"email: {old_user.email} → {instance.email}")

            if old_user.is_active != instance.is_active:
                changes.append(f"is_active: {old_user.is_active} → {instance.is_active}")

            if changes:
                UserActionLog.objects.create(
                    user=instance,
                    action=f"Profile updated: {', '.join(changes)}",
                    ip_address=None
                )

        except CustomUser.DoesNotExist:
            pass


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Отправляет приветственное письмо при активации аккаунта
    """
    if created and instance.is_active and instance.email_verified:
        subject = _('Welcome to MMORPG Portal!')
        message = _(
            'Hello {}!\n\n'
            'Welcome to our MMORPG community portal!\n\n'
            'Now you can:\n'
            '- Create posts and announcements\n'
            '- Respond to other players\' posts\n'
            '- Subscribe to categories and news\n'
            '- Communicate with the community\n\n'
            'Best regards,\n'
            'MMORPG Portal Team'
        ).format(instance.first_name or instance.email)

        # Для разработки - вывод в консоль
        print(f"\n=== WELCOME EMAIL ===")
        print(f"To: {instance.email}")
        print(f"Subject: {subject}")
        print("Body:")
        print(message)
        print("=====================\n")

        # Отправляем настоящее письмо
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )


@receiver(post_save, sender=UserActionLog)
def notify_admin_on_important_actions(sender, instance, created, **kwargs):
    """
    Уведомляет админа о важных действиях пользователей
    """
    if created:
        important_keywords = ['delete', 'deactivate', 'password', 'login failed']
        action_lower = instance.action.lower()

        if any(keyword in action_lower for keyword in important_keywords):
            # Для разработки - вывод в консоль
            print(f"\n=== ADMIN NOTIFICATION ===")
            print(f"Important action detected: {instance.action}")
            print(f"User: {instance.user.email if instance.user else 'Anonymous'}")
            print(f"IP: {instance.ip_address}")
            print(f"Time: {instance.timestamp}")
            print("==========================\n")

            # Здесь можно добавить отправку email админу
            # send_mail_to_admin(instance)
