"""
Module containing Django test cases for room reservations in the application.

Classes:
- DormRoomTestCase: Test case for the DormRoom model.
- RoomReservationTestCase: Test case for the RoomReservation model.

Author: [ASF]
Creation Date: [13.11.2023]
"""

from django.test import TestCase
from django.contrib.auth.models import User
from reservation.models import DormRoom, RoomReservation
from datetime import datetime, timedelta


class DormRoomTestCase(TestCase):
    """
        Test case for the DormRoom model.

        Methods:
        - setUp(): Prepares data for testing.
        - test_get_beds(): Tests the get_beds method.
        - test_get_bathroom_type(): Tests the get_bathroom_type method.
        - test_get_mini_kitchenette(): Tests the get_mini_kitchenette method.
        - test_is_available(): Tests the is_available method for room reservation availability.
        """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.room = DormRoom.objects.create(city='TestCity', room_type='single', mini_kitchenette=True,
                                            private_bathroom=True, price=500.00)

    def test_get_beds(self):
        self.assertEqual(self.room.get_beds(), 1)

    def test_get_bathroom_type(self):
        self.assertEqual(self.room.get_bathroom_type(), 'Private')

    def test_get_mini_kitchenette(self):
        self.assertEqual(self.room.get_mini_kitchenette(), 'Yes')

    def test_is_available(self):
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=7)
        self.assertTrue(self.room.is_available(start_date, end_date))


class RoomReservationTestCase(TestCase):
    """
        Test case for the RoomReservation model.

        Methods:
        - setUp(): Prepares data for testing.
        - test_is_open_reservation(): Tests the is_open_reservation method.
        """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.room = DormRoom.objects.create(city='TestCity', room_type='single', mini_kitchenette=True,
                                            private_bathroom=True, price=500.00)

        self.reservation = RoomReservation.objects.create(user=self.user, room=self.room,
                                                          check_in_date=datetime.now().date(),
                                                          check_out_date=datetime.now().date() + timedelta(days=1),
                                                          number_of_people=1)

    def test_is_open_reservation(self):
        self.assertTrue(self.reservation.is_open_reservation())
