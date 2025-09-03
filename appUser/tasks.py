from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def clean_expired_verifications():
    """Очистка просроченных верификаций"""
    from .models import EmailVerification

    expired_time = timezone.now() - timedelta(hours=24)
    expired_verifications = EmailVerification.objects.filter(
        created_at__lt=expired_time
    )

    count = 0
    for verification in expired_verifications:
        try:
            user = verification.user
            verification.delete()
            logger.info(f"Deleted expired verification for user {user.email}")
            count += 1
        except Exception as e:
            logger.error(f"Error deleting verification {verification.id}: {e}")

    return f'Cleaned {count} expired verifications'


@shared_task
def clean_old_user_logs():
    """Очистка старых логов пользователей"""
    from .models import UserActionLog
    from django.utils import timezone
    from datetime import timedelta

    try:
        cutoff_date = timezone.now() - timedelta(days=90)
        old_logs = UserActionLog.objects.filter(timestamp__lt=cutoff_date)
        count = old_logs.count()

        old_logs.delete()

        logger.info(f'Cleaned {count} old user logs')
        return f'Cleaned {count} old user logs'

    except Exception as e:
        logger.error(f"Error cleaning old user logs: {e}")
        return f'Error: {e}'
