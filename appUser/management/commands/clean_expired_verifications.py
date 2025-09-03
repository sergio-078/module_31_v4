from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from appUser.models import EmailVerification

class Command(BaseCommand):
    help = 'Clean up expired email verifications'

    def handle(self, *args, **options):
        expired_time = timezone.now() - timedelta(hours=24)
        expired_verifications = EmailVerification.objects.filter(
            created_at__lt=expired_time
        )

        count = expired_verifications.count()
        expired_verifications.delete()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} expired verifications')
        )
