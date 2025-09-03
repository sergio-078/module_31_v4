"""
Local settings for proNotification project.
This file is for machine-specific settings and should be in .gitignore.
"""

from .base import *

# Local database settings (if different from default)
# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'mmorpg_local',
#     'USER': 'your_username',
#     'PASSWORD': 'your_password',
#     'HOST': 'localhost',
#     'PORT': '5432',
# }

# Local email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_app_password'

# Local Celery settings
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Debug settings for local development
DEBUG = True

# Additional apps for local development
INSTALLED_APPS += [

]

# Allow all hosts for local development
ALLOWED_HOSTS = ['*']

print("Local settings loaded")
