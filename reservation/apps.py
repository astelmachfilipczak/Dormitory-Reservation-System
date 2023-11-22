"""
Django application configuration for the room reservation application.

Configures the default auto field for models and sets the application name.

Author: [ASF]
Creation Date: [13.11.2023]
"""

from django.apps import AppConfig


class ReservationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservation'
