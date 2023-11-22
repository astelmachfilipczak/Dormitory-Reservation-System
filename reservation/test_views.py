"""
Module containing Django test cases for room reservations in the application.

Classes:
- IndexViewTests: Test case for the index view.
- AboutViewTests: Test case for the about_view.
- ContactViewTests: Test case for the contact view.
- MyReservationViewTests: Test case for the my_reservation view.
- ReservationViewTests: Test case for the reservation view.
- RegistrationViewTest: Test case for the registration view.
- LoginLogoutViewTest: Test case for the login and logout views.
- SearchViewTest: Test case for the search view.
- RoomsViewTest: Test case for the rooms view.

Author: [ASF]
Creation Date: [21.11.2023]
"""

from datetime import timedelta
from django.test import TestCase, Client
from django.utils import timezone
from django.template import TemplateDoesNotExist
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.messages import get_messages
from .models import DormRoom, RoomReservation
from .forms import RoomReservationForm


class IndexViewTests(TestCase):
    """
    Test case for the index view.

    Methods:
    - setUp: Set up initial data for testing.
    - test_index_view_uses_correct_template: Test if the index view uses the correct template.
    - test_index_view_returns_five_random_rooms: Test if the index view returns five random rooms.
    """

    def setUp(self):

        self.initial_data = [
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

        ]

        for data in self.initial_data:
            room = DormRoom(**data)
            room.save()

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_returns_five_random_rooms(self):
        response = self.client.get(reverse('index'))
        room_data = response.context['room_data']

        self.assertEqual(len(room_data), 5)

        for room in room_data:
            self.assertIsInstance(room, DormRoom)


class AboutViewTests(TestCase):
    """
        Test case for the about_view.

        This test case includes tests for the about_view, which displays information about the
        application.

        Methods:
        - test_about_view: Test if the about_view returns the correct response.
        - test_about_view_template_exists: Test if the about_view template exists.
        """

    def test_about_view(self):

        client = Client()

        url = reverse('about')
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_about_view_template_exists(self):

        try:
            template = self.client.get(reverse('about')).templates[0]
        except TemplateDoesNotExist:
            template = None

        self.assertIsNotNone(template)


class ContactViewTests(TestCase):
    """
       Test case for the contact view.

       This test case includes tests for the contact view, which provides contact information.

       Methods:
       - test_contact_view: Test if the contact view returns the correct response.
       - test_contact_view_template_exists: Test if the contact view template exists.
       """

    def test_contact_view(self):

        client = Client()

        url = reverse('contact')
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_contact_view_template_exists(self):

        try:
            template = self.client.get(reverse('contact')).templates[0]
        except TemplateDoesNotExist:
            template = None

        self.assertIsNotNone(template)


class MyReservationViewTests(TestCase):
    """
        Test case for the myreservation view.

        This test case includes tests for the my_reservation view, which displays
        reservations made by the authenticated user.

        Methods:
        - setUp: Set up initial data for testing.
        - test_authenticated_user_view: Test if the myreservation view displays reservations for authenticated users.
        - test_unauthenticated_user_redirect: Test if unauthenticated users are redirected to the login page.
        - tearDown: Clean up data after testing.
        """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.today = timezone.now().date()
        self.room_id = 1
        check_in_date = self.today - timedelta(days=2)
        check_out_date_open = self.today + timedelta(days=5)
        check_out_date_closed = self.today - timedelta(days=1)

        self.open_reservation = RoomReservation.objects.create(
            user=self.user,
            room_id=self.room_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date_open
        )

        self.closed_reservation = RoomReservation.objects.create(
            user=self.user,
            room_id=self.room_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date_closed
        )

        self.client = Client()

    def test_authenticated_user_view(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('myreservation')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('open_reservations', response.context)
        self.assertIn('closed_reservations', response.context)

    def test_unauthenticated_user_redirect(self):
        url = reverse('myreservation')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def tearDown(self):
        self.user.delete()
        self.open_reservation.delete()
        self.closed_reservation.delete()


class ReservationViewTests(TestCase):
    """
        Test case for the reservation view.

        This test case includes tests for the reservation view, which allows users
        to make reservations for dormitory rooms.

        Methods:
        - setUp: Set up initial data for testing.
        - test_authenticated_user_view_GET: Test if authenticated users can access the reservation view (GET).
        - test_authenticated_user_view_POST_valid_form: Test if authenticated users can make a reservation with a valid
        form (POST).
        - test_authenticated_user_view_POST_invalid_form: Test if authenticated users receive errors with an invalid
        form (POST).
        - test_authenticated_user_view_POST_room_already_taken: Test if users receive an error when trying to reserve
        an already taken room.
        """

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.room = DormRoom.objects.create(id=1, city='City', room_type='double', private_bathroom='True',
                                            mini_kitchenette='True', price=700.00)
        self.url = reverse('reservation', args=[self.room.id])
        self.today = timezone.now().date()

    def test_authenticated_user_view_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Make a reservation')
        self.assertContains(response, 'City - Room 1')
        self.assertIsInstance(response.context['form'], RoomReservationForm)
        self.assertQuerysetEqual(response.context['open_reservations'], [])
        self.assertQuerysetEqual(response.context['closed_reservations'], [])

    def test_authenticated_user_view_POST_valid_form(self):
        self.client.force_login(self.user)
        check_in_date = self.today + timedelta(days=1)
        check_out_date = self.today + timedelta(days=3)
        data = {'check_in_date': check_in_date,
                'check_out_date': check_out_date,
                'room': self.room.id,
                'number_of_people': 1
                }
        response = self.client.post(self.url, data, follow=True)

        expected_url = reverse('myreservation')
        self.assertContains(response, expected_url)

        self.assertTrue(RoomReservation.objects.filter(user=self.user, room=self.room).exists())

    def test_authenticated_user_view_POST_invalid_form(self):
        self.client.force_login(self.user)
        data = {'check_in_date': self.today,
                'check_out_date': self.today - timedelta(days=1),
                'room': self.room.id,
                'number_of_people': 1
                }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Make a reservation')
        self.assertContains(response, 'City - Room 1')
        self.assertIsInstance(response.context['form'], RoomReservationForm)

    def test_authenticated_user_view_POST_room_already_taken(self):
        self.client.force_login(self.user)

        room = DormRoom.objects.create(id=2, city='City', room_type='double', private_bathroom=True,
                                       mini_kitchenette=True, price=700.00, image_name='room-1.jpg')

        existing_reservation = RoomReservation.objects.create(
            user=self.user,
            room=room,
            check_in_date=self.today + timedelta(days=1),
            check_out_date=self.today + timedelta(days=3),
            number_of_people=1,
            is_open=True
        )

        data = {
            'check_in_date': self.today,
            'check_out_date': self.today + timedelta(days=2),
            'room': room.id,
            'number_of_people': 3
        }

        response = self.client.post(reverse('reservation', args=[room.id]), data)

        self.assertTrue(RoomReservation.objects.filter(id=existing_reservation.id).exists())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room already taken', status_code=200)
        self.assertIsInstance(response.context['form'], RoomReservationForm)


class RegistrationViewTest(TestCase):
    """
        Test case for the registration view.

        This test case includes tests for user registration.

        Methods:
        - test_registration_success: Test if user registration is successful.
        - test_registration_password_mismatch: Test if user registration fails with password mismatch.
        """

    def test_registration_success(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password2': 'testpassword',
        }

        response = self.client.post(reverse('register'), data)

        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_password_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password2': 'mismatchedpassword',
        }

        response = self.client.post(reverse('register'), data)

        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertEqual(response.status_code, 302)


class LoginLogoutViewTest(TestCase):
    """
        Test case for the login and logout views.

        This test case includes tests for user login, logout, and related functionality.

        Methods:
        - setUp: Set up initial data for testing.
        - test_login_success: Test if user login is successful.
        - test_login_failure: Test if user login fails with incorrect credentials.
        - test_logout: Test if user logout is successful.
        """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        response = self.client.post(reverse('login'), data)

        self.assertIn(auth.SESSION_KEY, self.client.session)

        self.assertRedirects(response, reverse('index'))

    def test_login_failure(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

        response = self.client.post(reverse('login'), data)

        self.assertNotIn(auth.SESSION_KEY, self.client.session)
        self.assertRedirects(response, reverse('login'))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Credentials Invalid', messages)

    def test_logout(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('logout'))

        self.assertNotIn(auth.SESSION_KEY, self.client.session)
        self.assertRedirects(response, reverse('index'))


class SearchViewTest(TestCase):
    """
        Test case for the search view.

        This test case includes tests for searching and filtering dormitory rooms.

        Methods:
        - setUp: Set up initial data for testing.
        - test_search_view_get: Test if the search view is accessible (GET).
        - test_search_view_post: Test if searching by keyword returns results (POST).
        - test_search_view_post_no_results: Test if searching with no results returns an empty list (POST).
        - test_search_view_post_with_filters: Test if searching with filters returns results (POST).
        """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.room = DormRoom.objects.create(id=1, city='City', room_type='single', private_bathroom=True,
                                            mini_kitchenette=True, price=500.00, image_name='room-1.jpg')

    def test_search_view_get(self):
        response = self.client.get(reverse('search'))

        self.assertEqual(response.status_code, 200)

    def test_search_view_post(self):
        response = self.client.post(reverse('search'), data={'keyword': 'City'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('room_data', response.context)
        self.assertIn(self.room, response.context['room_data'])

    def test_search_view_post_no_results(self):
        response = self.client.post(reverse('search'), data={'keyword': 'NonExistentCity'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('room_data', response.context)
        self.assertNotIn(self.room, response.context['room_data'])

    def test_search_view_post_with_filters(self):
        response = self.client.post(reverse('search'), data={
            'keyword': 'City',
            'arrival_departure': '2023-12-01 to 2023-12-05',
            'city': 'City',
            'room_type': 'Single',
            'mini_kitchenette': 'Yes',
            'private_bathroom': 'Yes',
            'price': '500 PLN',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('room_data', response.context)
        self.assertIn(self.room, response.context['room_data'])


class RoomsViewTest(TestCase):
    """
       Test case for the rooms view.

       This test case includes tests for displaying dormitory rooms.

       Methods:
       - setUp: Set up initial data for testing.
       - test_rooms_view_get: Test if the rooms view is accessible and returns room data (GET).
       - test_rooms_view_no_rooms: Test if the rooms view handles no available rooms gracefully (GET).
       """

    def setUp(self):
        DormRoom.objects.create(city='Warszawa', street='Nowy Świat', room_type='single', mini_kitchenette=False,
                                private_bathroom=False, price=500.00, image_name='room-1.jpg')
        DormRoom.objects.create(city='Kraków', street='Krupnicza', room_type='double', mini_kitchenette=True,
                                private_bathroom=True, price=700.00, image_name='room-2.jpg')

    def test_rooms_view_get(self):
        response = self.client.get(reverse('rooms'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('room_data', response.context)
        self.assertNotEqual(len(response.context['room_data']), 0)

    def test_rooms_view_no_rooms(self):
        DormRoom.objects.all().delete()

        response = self.client.get(reverse('rooms'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('room_data', response.context)
        self.assertEqual(len(response.context['room_data']), 0)
