"""
Django URL patterns for the Reservation App.

This module defines the URL patterns (routing) for the Reservation App views.

URL Patterns:
- '' : Index page.
- 'about' : About page.
- 'reservation/<int:room_id>/' : Room reservation page.
- 'my_reservation' : User's reservation page.
- 'register' : User registration page.
- 'login' : User login page.
- 'logout' : User logout page.
- 'contact' : Contact page.
- 'search' : Room search page.
- 'rooms' : All rooms page.
"""

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about_view, name='about'),
    path('reservation/<int:room_id>/', views.reservation_view, name='reservation'),
    path('my_reservation', views.my_reservation_view, name='myreservation'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('contact', views.contact_view, name='contact'),
    path('search', views.search_view, name='search'),
    path('rooms', views.rooms, name='rooms'),
]
