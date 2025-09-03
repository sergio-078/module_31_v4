from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from appUser.models import UserActionLog


class Command(BaseCommand):
    help = 'Clean up user action logs older than 90 days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Delete logs older than this number of days (default: 90)'
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)

        old_logs = UserActionLog.objects.filter(timestamp__lt=cutoff_date)
        count = old_logs.count()

        old_logs.delete()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} logs older than {days} days')
        )
