"""
Django URL configuration for the dormitory project.

Includes paths for the admin site and the reservation app.

Author: [ASF]
Creation Date: [13.11.2023]
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservation.urls')),
]
