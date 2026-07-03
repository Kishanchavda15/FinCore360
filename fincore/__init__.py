"""
project/__init__.py
--------------------
This makes Celery start when Django starts (required for @shared_task to work).
"""

from notifications_app.celery import app as celery_app

__all__ = ("celery_app",)