"""
Settings package for proNotification project.
This file imports the base settings and then tries to import environment-specific settings.
"""

from .celery import app as celery_app

__all__ = ('celery_app',)
