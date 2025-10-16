"""
This file contains the configuration for the Django application.

It includes the AppConfig class that sets up the application for use in
Django. By default, it defines the application's name and imports
necessary modules for the app's initialization.
"""

from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_auth'
