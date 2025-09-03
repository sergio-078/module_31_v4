"""
Example secret settings file.
Copy this file to secret.py and fill in your actual values.
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'generate-a-secure-random-key-here'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-database-name',
        'USER': 'your-database-user',
        'PASSWORD': 'your-database-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'

# Redis configuration
REDIS_URL = 'redis://localhost:6379/0'

# Add other settings as needed...
