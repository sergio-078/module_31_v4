"""
Development settings for proNotification project.
These settings are used during local development.
"""

from .base import *

# Debug settings
DEBUG = True

# Additional apps for development
INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

# Additional middleware for development
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Debug toolbar settings
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}

# Email settings for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database settings for development
# You can override database settings here if needed
# DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
# DATABASES['default']['NAME'] = 'mmorpg_dev'

# Simplified Celery settings for development
CELERY_TASK_ALWAYS_EAGER = True  # Execute tasks synchronously (without Celery)
CELERY_TASK_EAGER_PROPAGATES = True

# Cache settings for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# File upload settings for development
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Logging for development
LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['appUser']['level'] = 'DEBUG'
LOGGING['loggers']['appNotification']['level'] = 'DEBUG'

# Allow all hosts for development
ALLOWED_HOSTS = ['*']

# Django extensions settings
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True

print("Development settings loaded")
