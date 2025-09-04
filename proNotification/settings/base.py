"""
Base settings for proNotification project.
These settings are common to all environments.
"""

import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')

# Application definition
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # Third-party apps
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'crispy_bootstrap5',

    # Local apps
    'appUser',
    'appNotification',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # Custom middleware
    'appUser.middleware.UserIPMiddleware',
    'appUser.middleware.EmailVerificationMiddleware',
]

ROOT_URLCONF = 'proNotification.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'appNotification.context_processors.categories',
                'appNotification.context_processors.navigation_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'proNotification.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
]

TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Locale paths
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'appUser.CustomUser'

# Email settings
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@localhost')
SERVER_EMAIL = os.getenv('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# CKEditor settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'SpecialChar'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', 'Source'],
        ],
        'height': 300,
        'width': '100%',
        'removePlugins': 'stylesheetparser',
        'allowedContent': True,
        'extraAllowedContent': '*(*);*{*}',
        'disallowedContent': 'script; *[on*]',
        'contentsCss': ['/static/css/ckeditor.css'],
        'autoParagraph': False,
        'fillEmptyBlocks': False,
        'tabSpaces': 4,
        'language': 'ru',
    }
}

# Celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

# Celery beat schedule
CELERY_BEAT_SCHEDULE = {
    'clean-expired-verifications': {
        'task': 'appUser.tasks.clean_expired_verifications',
        'schedule': timedelta(hours=6),
    },
    'send-weekly-newsletter': {
        'task': 'appNotification.tasks.send_weekly_newsletter',
        'schedule': timedelta(seconds=30),  # For testing - every 30 seconds
    },
    'send-weekly-posts-digest': {
        'task': 'appNotification.tasks.send_weekly_posts_digest',
        'schedule': timedelta(seconds=45),  # For testing - every 45 seconds
    },
    'clean-old-user-logs': {
        'task': 'appUser.tasks.clean_old_user_logs',
        'schedule': timedelta(days=7),  # Once a week
    },
}

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Site settings
SITE_ID = 1
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000')
SITE_NAME = os.getenv('SITE_NAME', 'MMORPG Portal')

# Login/Logout settings
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/user/login/'

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Security settings (overridden in production)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# File upload settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'appUser': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'appNotification': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
