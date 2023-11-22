"""
Module for configuring the Django admin interface for the room reservation application.

Registers the following models with the admin interface:
- DormRoom: Allows admin users to manage dormitory room details.
- RoomReservation: Allows admin users to view and manage user reservations for dormitory rooms.

Author: [ASF]
Creation Date: [13.11.2023]
"""

from django.contrib import admin
from .models import DormRoom, RoomReservation

admin.site.register(DormRoom)
admin.site.register(RoomReservation)