from django.apps import AppConfig

class AppuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appUser'

    def ready(self):
        # Импортируем и регистрируем сигналы
        import appUser.signals
