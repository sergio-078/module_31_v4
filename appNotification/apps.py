from django.apps import AppConfig


class AppnotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appNotification'

    def ready(self):
        import appNotification.signals
