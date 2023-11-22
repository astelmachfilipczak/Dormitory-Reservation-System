"""
Module containing Django views responsible for handling room reservations in the application.

Views:
- index(request): Renders the main page with a random selection of rooms.
- about_view(request): Renders the informational about page.
- my_reservation_view(request): Renders the page displaying user's reservations, both current and past.
- reservation_view(request, room_id): Handles room reservation, both displaying the form and saving the reservation.
- register(request): Handles the user registration process.
- login(request): Handles the user login process.
- logout(request): Handles the user logout process.
- contact_view(request): Renders the contact page.
- search_view(request): Handles room search based on user input.
- rooms(request): Renders the page with all available rooms.

The module uses the DormRoom and RoomReservation models from the 'reservation' app, forms, and HTML templates
for user interaction. Additionally, it includes helper functions for processing reservation-related data.

Author: [ASF]
Creation Date: [13.11.2023]
"""

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.utils import timezone
from reservation.forms import RoomReservationForm
from reservation.models import DormRoom, RoomReservation
from random import sample
import decimal
from datetime import datetime


def index(request):
    """
    View for rendering the index page with a random selection of dormitory rooms.

    Parameters:
    - request: HttpRequest object

    Returns:
    - Rendered HTML page with a random selection of rooms.
    """

    initial_data = [
        {'city': 'Warszawa', 'street': 'Nowy Świat', 'room_type': 'single', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 500.00, 'image_name': 'room-1.jpg'},
        {'city': 'Kraków', 'street': 'Krupnicza', 'room_type': 'single', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 500.00, 'image_name': 'room-2.jpg'},
        {'city': 'Poznań', 'street': 'Stary Rynek', 'room_type': 'single', 'mini_kitchenette': False,
         'private_bathroom': True,
         'price': 700.00, 'image_name': 'room-3.jpg'},
        {'city': 'Warszawa', 'street': 'Nowy Świat', 'room_type': 'single', 'mini_kitchenette': False,
         'private_bathroom': True,
         'price': 700.00, 'image_name': 'room-4.jpg'},
        {'city': 'Poznań', 'street': 'Stary Rynek', 'room_type': 'single', 'mini_kitchenette': True,
         'private_bathroom': True,
         'price': 700.00, 'image_name': 'room-5.jpg'},
        {'city': 'Warszawa', 'street': 'Nowy Świat', 'room_type': 'double', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 400.00, 'image_name': 'room-6.jpg'},
        {'city': 'Kraków', 'street': 'Krupnicza', 'room_type': 'double', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 400.00, 'image_name': 'room-7.jpg'},
        {'city': 'Kraków', 'street': 'Krupnicza', 'room_type': 'single', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 500.00, 'image_name': 'room-8.jpg'},
        {'city': 'Poznań', 'street': 'Stary Rynek', 'room_type': 'double', 'mini_kitchenette': True,
         'private_bathroom': False,
         'price': 400.00, 'image_name': 'room-9.jpg'},
        {'city': 'Warszawa', 'street': 'Nowy Świat', 'room_type': 'triple', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 300.00, 'image_name': 'room-10.jpg'},
        {'city': 'Kraków', 'street': 'Krupnicza', 'room_type': 'single', 'mini_kitchenette': False,
         'private_bathroom': True,
         'price': 700.00, 'image_name': 'room-11.jpg'},
        {'city': 'Kraków', 'street': 'Krupnicza', 'room_type': 'double', 'mini_kitchenette': False,
         'private_bathroom': True,
         'price': 400.00, 'image_name': 'room-12.jpg'},
        {'city': 'Poznań', 'street': 'Stary Rynek', 'room_type': 'single', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 500.00, 'image_name': 'room-13.jpg'},
        {'city': 'Szczecin', 'street': 'Krzywoustego', 'room_type': 'single', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 500.00, 'image_name': 'room-14.jpg'},
        {'city': 'Szczecin', 'street': 'Krzywoustego', 'room_type': 'single', 'mini_kitchenette': True,
         'private_bathroom': True,
         'price': 700.00, 'image_name': 'room-15.jpg'},
        {'city': 'Szczecin', 'street': 'Krzywoustego', 'room_type': 'single', 'mini_kitchenette': True,
         'private_bathroom': True,
         'price': 700.00, 'image_name': 'room-16.jpg'},
        {'city': 'Szczecin', 'street': 'Krzywoustego', 'room_type': 'single', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 500.00, 'image_name': 'room-17.jpg'},
        {'city': 'Poznań', 'street': 'Stary Rynek', 'room_type': 'single', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 500.00, 'image_name': 'room-18.jpg'},
        {'city': 'Warszawa', 'street': 'Nowy Świat', 'room_type': 'double', 'mini_kitchenette': True,
         'private_bathroom': True,
         'price': 400.00, 'image_name': 'room-19.jpg'},
        {'city': 'Kraków', 'street': 'Krupnicza', 'room_type': 'double', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 400.00, 'image_name': 'room-20.jpg'},
        {'city': 'Poznań', 'street': 'Stary Rynek', 'room_type': 'triple', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 300.00, 'image_name': 'room-21.jpg'},
        {'city': 'Warszawa', 'street': 'Nowy Świat', 'room_type': 'triple', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 300.00, 'image_name': 'room-22.jpg'},
        {'city': 'Kraków', 'street': 'Krupnicza', 'room_type': 'triple', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 300.00, 'image_name': 'room-23.jpg'},
        {'city': 'Szczecin', 'street': 'Krzywoustego', 'room_type': 'triple', 'mini_kitchenette': False,
         'private_bathroom': False,
         'price': 300.00, 'image_name': 'room-24.jpg'},
    ]

    if not DormRoom.objects.exists():

        for data in initial_data:
            room = DormRoom(**data)
            room.save()

    all_rooms = list(DormRoom.objects.all())
    random_rooms = sample(all_rooms, 5)

    return render(request, 'index.html', {'room_data': random_rooms})


def about_view(request):
    """
        View for rendering the about page.

        Parameters:
        - request: HttpRequest object

        Returns:
        - Rendered HTML about page.
        """

    return render(request, 'about.html')


def my_reservation_view(request):
    """
        View for rendering user's reservations.

        Parameters:
        - request: HttpRequest object

        Returns:
        - Rendered HTML page displaying the user's open and closed reservations.
        """

    if request.user.is_authenticated:
        today = timezone.now().date()
        open_reservations = RoomReservation.objects.filter(user=request.user, check_out_date__gte=today)
        closed_reservations = RoomReservation.objects.filter(user=request.user, check_out_date__lt=today)

        return render(request, 'my_reservation.html',
                      {'open_reservations': open_reservations, 'closed_reservations': closed_reservations})
    else:
        return redirect('login')

def reservation_view(request, room_id):
    """
        View for handling room reservations.

        Parameters:
        - request: HttpRequest object
        - room_id: int, ID of the selected room

        Returns:
        - If the user is authenticated:
          - If the request method is POST:
            - If the form is valid, save the reservation and redirect to 'myreservation' page.
              - If the room is already reserved for the selected dates, display an error message.
              - If the number of students is greater than number of beds, display an error message.
            - If the form is invalid, re-render the reservation page with the form and room details.
          - If the request method is GET, render the reservation page with an empty reservation form
            and details of the selected room, along with the user's open and closed reservations.
        - If the user is not authenticated, redirect to the 'login' page.
        """

    if request.user.is_authenticated:
        try:
            room = DormRoom.objects.get(id=room_id)
        except DormRoom.DoesNotExist:
            return redirect('rooms')

        if request.method == 'POST':
            form = RoomReservationForm(request.POST)
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.room = room

                today = timezone.now().date()
                if today > reservation.check_out_date:
                    reservation.is_open = False
                else:
                    reservation.is_open = True

                if reservation.number_of_people > room.get_beds():
                    messages.error(request, 'Room is too small for the specified number of guests')
                    return render(request, 'reservation.html', {'form': form, 'room': room})

                if RoomReservation.objects.filter(room=room, is_open=True,
                                                  check_in_date__lte=reservation.check_out_date,
                                                  check_out_date__gte=reservation.check_in_date).exists():
                    messages.error(request, 'Room already taken')
                    return render(request, 'reservation.html', {'form': form, 'room': room})

                reservation.save()
                return redirect('myreservation')

            else:
                form = RoomReservationForm(initial={'room': room.id})
                return render(request, 'reservation.html', {'form': form, 'room': room})

        else:
            form = RoomReservationForm()

        open_reservations = RoomReservation.objects.filter(user=request.user, is_open=True)
        closed_reservations = RoomReservation.objects.filter(user=request.user, is_open=False)

        return render(request, 'reservation.html',
                      {'form': form, 'room': room, 'open_reservations': open_reservations,
                       'closed_reservations': closed_reservations})

    else:
        return redirect('login')

def register(request):
    """
       View for user registration.

       Parameters:
       - request: HttpRequest object

       Returns:
       - Rendered HTML registration page or redirect to login page.
       """

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password Not The Same')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    """
        View for user login.

        Parameters:
        - request: HttpRequest object

        Returns:
        - Redirect to the home page or re-render the login page with an error message.
        """

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    """
        View for user logout.

        Parameters:
        - request: HttpRequest object

        Returns:
        - Redirect to the home page.
        """

    auth.logout(request)
    return redirect('/')


def contact_view(request):
    """
        View for rendering the contact page.

        Parameters:
        - request: HttpRequest object

        Returns:
        - Rendered HTML contact page.
        """

    return render(request, 'contact.html')


def search_view(request):
    """
       View for handling room search based on user input.

       Parameters:
       - request: HttpRequest object

       Returns:
       - Rendered HTML search results page.
       """

    filtered_data = DormRoom.objects.all()

    keyword = request.POST.get('keyword')
    arrival_departure = request.POST.get('arrival_departure')
    city = request.POST.get('city')
    room_type = request.POST.get('room_type')
    mini_kitchenette = request.POST.get('mini_kitchenette')
    private_bathroom = request.POST.get('private_bathroom')
    price = request.POST.get('price')

    if keyword:
        keyword = keyword.lower()
        filtered_data = filtered_data.filter(city__icontains=keyword)

    if arrival_departure:
        start_date, end_date = map(lambda x: datetime.strptime(x.strip(), '%Y-%m-%d'), arrival_departure.split(' to '))
        filtered_data = DormRoom.objects.filter(
            id__in=[room.id for room in filtered_data if room.is_available(start_date, end_date)])

    if city:
        filtered_data = filtered_data.filter(city=city)

    if room_type:
        if room_type == 'Single':
            filtered_data = filtered_data.filter(room_type='single')
        elif room_type == 'Double':
            filtered_data = filtered_data.filter(room_type='double')
        elif room_type == 'Triple':
            filtered_data = filtered_data.filter(room_type='triple')

    if mini_kitchenette:
        if mini_kitchenette == 'Yes':
            filtered_data = filtered_data.filter(mini_kitchenette=True)
        elif mini_kitchenette == 'No':
            filtered_data = filtered_data.filter(mini_kitchenette=False)

    if private_bathroom:
        if private_bathroom == 'Yes':
            filtered_data = filtered_data.filter(private_bathroom=True)
        elif private_bathroom == 'No':
            filtered_data = filtered_data.filter(private_bathroom=False)

    if price:
        if price == 'Unlimited':
            filtered_data = filtered_data.all()
        else:
            price = decimal.Decimal(price.replace(' PLN', '').replace(',', ''))
            filtered_data = filtered_data.filter(price=price)

    return render(request, 'search.html', {'room_data': filtered_data})


def rooms(request):
    """
        View for rendering the rooms page with all available rooms.

        Parameters:
        - request: HttpRequest object

        Returns:
        - Rendered HTML rooms page.
        """
    all_rooms = list(DormRoom.objects.all())
    return render(request, 'rooms.html', {'room_data': all_rooms})

