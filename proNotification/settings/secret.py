"""
Secret settings for proNotification project.
This file contains sensitive information and should NEVER be committed to version control.
Add this file to .gitignore and keep it secure.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-super-secret-key-here-change-this-in-production'

# Database configuration (PostgreSQL example)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mmorpg_database',
        'USER': 'mmorpg_user',
        'PASSWORD': 'your-database-password-here',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Email configuration (Gmail example)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password-here'  # Use app password, not regular password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
SERVER_EMAIL = 'your-email@gmail.com'

# Redis configuration for Celery
REDIS_URL = 'redis://localhost:6379/0'
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
        },
        'KEY_PREFIX': 'mmorpg_prod',
    }
}

# AWS S3 configuration (if using S3 for media files)
AWS_ACCESS_KEY_ID = 'your-aws-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-aws-secret-access-key'
AWS_STORAGE_BUCKET_NAME = 'your-s3-bucket-name'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

# Social authentication keys (if using social auth)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-google-oauth2-key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-google-oauth2-secret'

SOCIAL_AUTH_FACEBOOK_KEY = 'your-facebook-app-id'
SOCIAL_AUTH_FACEBOOK_SECRET = 'your-facebook-app-secret'

SOCIAL_AUTH_VK_OAUTH2_KEY = 'your-vk-app-id'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'your-vk-app-secret'

# Payment system keys (if integrating payments)
STRIPE_PUBLISHABLE_KEY = 'pk_test_your-stripe-publishable-key'
STRIPE_SECRET_KEY = 'sk_test_your-stripe-secret-key'
STRIPE_WEBHOOK_SECRET = 'whsec_your-stripe-webhook-secret'

# SMS service configuration (if using SMS)
TWILIO_ACCOUNT_SID = 'your-twilio-account-sid'
TWILIO_AUTH_TOKEN = 'your-twilio-auth-token'
TWILIO_PHONE_NUMBER = '+1234567890'

# API keys for external services
GOOGLE_MAPS_API_KEY = 'your-google-maps-api-key'
RECAPTCHA_PUBLIC_KEY = 'your-recaptcha-site-key'
RECAPTCHA_PRIVATE_KEY = 'your-recaptcha-secret-key'

# Admin and monitoring
ADMINS = [
    ('Admin Name', 'admin@example.com'),
    ('DevOps', 'devops@example.com'),
]

MANAGERS = ADMINS

SENTRY_DSN = 'your-sentry-dsn-url-here'

# Security-sensitive settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database encryption key (for encrypted fields)
FIELD_ENCRYPTION_KEY = 'your-32-char-encryption-key-here='  # Must be 32 url-safe base64-encoded bytes

# JWT secret for API authentication
JWT_SECRET_KEY = 'your-jwt-secret-key-for-api-auth'

# API rate limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_CACHE_PREFIX = 'rl_'

# Logging configuration
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
        'json': {
            'format': {
                'level': '%(levelname)s',
                'time': '%(asctime)s',
                'module': '%(module)s',
                'process': '%(process)d',
                'thread': '%(thread)d',
                'message': '%(message)s',
            },
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'error.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'error_file', 'mail_admins', 'sentry'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'mail_admins', 'sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
        'appUser': {
            'handlers': ['file', 'error_file', 'sentry'],
            'level': 'INFO',
            'propagate': False,
        },
        'appNotification': {
            'handlers': ['file', 'error_file', 'sentry'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Monitoring and analytics
GOOGLE_ANALYTICS_ID = 'UA-XXXXXXXXX-X'
YANDEX_METRIKA_ID = 'XXXXXXXX'

# CDN configuration
CDN_ENABLED = True
CDN_DOMAIN = 'https://cdn.yourdomain.com'
STATIC_CDN_DOMAIN = CDN_DOMAIN
MEDIA_CDN_DOMAIN = CDN_DOMAIN

# Backup configuration
BACKUP_LOCATION = '/backups/mmorpg/'
BACKUP_ENCRYPTION_KEY = 'your-backup-encryption-key'

# Performance tuning
DATABASE_CONNECTION_POOL_SIZE = 10
DATABASE_CONNECTION_MAX_OVERFLOW = 20
DATABASE_CONNECTION_TIMEOUT = 30

# Feature flags
FEATURE_NEW_UI = False
FEATURE_PAYMENTS = False
FEATURE_SOCIAL_LOGIN = False
FEATURE_PREMIUM_SUBSCRIPTION = False

# Custom business logic settings
MAX_POSTS_PER_USER = 10
MAX_RESPONSES_PER_POST = 50
POST_EXPIRY_DAYS = 30
NEW_USER_LIMIT_PER_DAY = 5

print("Secret settings loaded - DO NOT COMMIT THIS FILE TO VERSION CONTROL!")
